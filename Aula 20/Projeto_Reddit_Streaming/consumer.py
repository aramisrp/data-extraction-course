import os
import json
import time
import pandas as pd
from datetime import datetime
from confluent_kafka import Consumer, KafkaError

# Configuração do Kafka (Consumidor)
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'reddit-datalake-consumer',
    'auto.offset.reset': 'earliest' # Se começar agora, tenta ler do começo
}
consumer = Consumer(conf)

TOPIC = 'reddit-stream'
consumer.subscribe([TOPIC])

# Diretório raiz do nosso Data Lake local
DATALAKE_ROOT = 'data_lake/raw/reddit'
os.makedirs(DATALAKE_ROOT, exist_ok=True)

# Parâmetros de Lote (Batching) para criação do Parquet
BATCH_SIZE = 20 # Número de mensagens por arquivo Parquet (em produção isso costuma ser maior ex: 100000)
FLUSH_INTERVAL_SECONDS = 30 # Ou a cada X segundos
messages_batch = []
last_flush_time = time.time()

def save_to_parquet(batch_data):
    """Recebe uma lista de dicionários, cria o DataFrame e salva em Parquet particionado por dia"""
    if not batch_data:
        return
        
    df = pd.DataFrame(batch_data)
    
    # Adicionando uma coluna para saber o momento da ingestão no nosso Data Lake
    df['ingestion_timestamp'] = pd.Timestamp.now()
    
    # Criando o particionamento (ano, mês, dia) simulando diretórios de S3/Cloud Storage
    hoje = datetime.now()
    partition_dir = f"{DATALAKE_ROOT}/ano={hoje.year}/mes={hoje.month:02d}/dia={hoje.day:02d}"
    os.makedirs(partition_dir, exist_ok=True)
    
    # Nome do arquivo único gerado pelo Timestamp (millisegundos)
    filename = f"{partition_dir}/batch_{int(time.time()*1000)}.parquet"
    
    # Salvando os dados no formato Parquet
    df.to_parquet(filename, index=False, engine='pyarrow', compression='snappy')
    print(f"🔥 Lote de {len(df)} registros gravados com sucesso em formato Parquet!")
    print(f"-> Arquivo criado: {filename}\n")

print(f"Iniciando gravação no Data Lake. Aguardando mensagens do tópico: {TOPIC}...")

try:
    while True:
        # Pede mensagens ao Kafka (espera até 1 segundo se não houver nada)
        msg = consumer.poll(1.0)
        
        current_time = time.time()
        
        # Lógica de gravação se atingirmos limite de tempo e tivermos dados pendentes
        if current_time - last_flush_time > FLUSH_INTERVAL_SECONDS and len(messages_batch) > 0:
            print("Tempo limite do lote atingido.")
            save_to_parquet(messages_batch)
            messages_batch.clear()
            last_flush_time = current_time
            
        if msg is None:
            continue
            
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            elif msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                print(f"Tópico '{TOPIC}' ainda não existe. Aguardando o Produtor enviar os primeiros dados...")
                time.sleep(2)
                continue
            else:
                print(msg.error())
                break
                
        # Sucesso! Temos uma mensagem.
        # Descompacta o payload que foi enviado pelo Produtor como String -> JSON(Dictionary)
        try:
            payload = json.loads(msg.value().decode('utf-8'))
            messages_batch.append(payload)
            print(f"Nova mensagem recebida do autor: /u/{payload.get('author')}")
            
            # Se o lote chegou no tamanho definido, salvamos no Parquet!
            if len(messages_batch) >= BATCH_SIZE:
                print(f"Tamanho do lote atingido ({BATCH_SIZE}).")
                save_to_parquet(messages_batch)
                messages_batch.clear()
                last_flush_time = current_time
                
        except Exception as e:
            print(f"Erro ao converter mensagem: {e}")

except KeyboardInterrupt:
    print("\nEncerrando consumidor do Data Lake...")
    # Tenta salvar mensagens que ficaram sobrando na memória ao cancelar
    if len(messages_batch) > 0:
        print("Salvando lote residual antes de sair...")
        save_to_parquet(messages_batch)
finally:
    # Fecha a conexão com o Kafka
    consumer.close()
