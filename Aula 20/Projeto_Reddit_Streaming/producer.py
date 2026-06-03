import time
import json
import requests
from confluent_kafka import Producer

# Configuração do Kafka (Produtor)
conf = {
    'bootstrap.servers': 'localhost:9092',  # Conecta ao listener externo do Docker no Windows
    'client.id': 'reddit-python-producer'
}
producer = Producer(conf)

# Tópico de destino
TOPIC = 'reddit-stream'

def delivery_report(err, msg):
    """Callback executado ao confirmar se a mensagem foi entregue ou falhou"""
    if err is not None:
        print(f"Erro ao enviar mensagem: {err}")
    else:
        print(f"Mensagem enviada para o tópico {msg.topic()} [partição {msg.partition()}]")

# API do Reddit: Acessando comentários mais recentes da comunidade
# IMPORTANTE: O Reddit exige um User-Agent personalizado para APIs públicas gratuitas.
headers = {
    'User-Agent': 'MonitoramentoAulasEngDados/1.0 (by /u/DataEngineeringInstructor)'
}
reddit_url = "https://www.reddit.com/r/brasil/comments.json?limit=10"

# Set (Conjunto) para guardar IDs de comentários já enviados e evitar repetições
processed_ids = set()

print(f"Iniciando Extração do Reddit (r/brasil) para o tópico: {TOPIC}...")

try:
    while True:
        try:
            response = requests.get(reddit_url, headers=headers)
            response.raise_for_status() # Verifica se houve erro HTTP (ex: 429 Too Many Requests)
            data = response.json()
            
            # Navega na estrutura JSON retornada pelo Reddit
            children = data.get('data', {}).get('children', [])
            
            new_count = 0
            # A API retorna do mais recente pro mais antigo (vamos processar ao contrário para respeitar a linha do tempo)
            for child in reversed(children):
                comment = child['data']
                comment_id = comment.get('id')
                
                # Só processamos se o ID ainda não tiver sido capturado
                if comment_id not in processed_ids:
                    # Montamos um payload limpo apenas com o que nos interessa para o Data Lake
                    payload = {
                        "id": comment_id,
                        "author": comment.get('author'),
                        "subreddit": comment.get('subreddit'),
                        "body": comment.get('body'),
                        "created_utc": comment.get('created_utc'),
                        "permalink": comment.get('permalink')
                    }
                    
                    # Convertendo o dicionário Python para String JSON
                    json_data = json.dumps(payload)
                    
                    # Produzindo a mensagem no Kafka
                    producer.produce(
                        topic=TOPIC, 
                        key=comment_id.encode('utf-8'), # A key garante que atualizações caiam na mesma partição (ordem)
                        value=json_data.encode('utf-8'),
                        callback=delivery_report
                    )
                    
                    processed_ids.add(comment_id)
                    new_count += 1
            
            # Força o envio dos dados em cache para o broker
            producer.poll(0)
            
            # Controle de memória: se a lista de IDs processados crescer muito, limpamos as antigas
            if len(processed_ids) > 10000:
                processed_ids.clear()
            
            if new_count == 0:
                print("Nenhum comentário novo nesta rodada...")

        except Exception as e:
            print(f"Erro na extração: {e}")
        
        # Espera 5 segundos antes da próxima requisição (para não ser bloqueado pela API gratuita)
        print("Aguardando 5 segundos...\n")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nEncerrando produtor de extração do Reddit...")
    # Garante que as últimas mensagens que ainda não foram transmitidas sejam enviadas antes do script morrer
    producer.flush()
