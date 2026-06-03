from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests
import json

# Definicao de argumentos padrao
default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# 1. Instanciacao da DAG usando a TaskFlow API (@dag) do Airflow 3
@dag(
    dag_id='pipeline_etl_clima_api',
    default_args=default_args,
    description='ETL completo com API externa e TaskFlow API (Airflow 3)',
    start_date=datetime(2026, 5, 10),
    schedule='@daily',
    catchup=False,
    tags=['aula17', 'etl', 'api']
)
def clima_etl_pipeline():
    """
    Pipeline de Dados (ETL)
    1. Extrai a temperatura atual de Brasilia via API Open-Meteo.
    2. Transforma os dados adicionando uma marca de tempo.
    3. Carrega os dados processados no banco de dados Postgres.
    """

    # Tarefa 0: Prepara o banco de dados (Cria tabela se nao existir)
    @task
    def criar_tabela():
        hook = PostgresHook(postgres_conn_id='postgres_default')
        sql = """
        CREATE TABLE IF NOT EXISTS tb_clima_brasilia (
            id SERIAL PRIMARY KEY,
            temperatura FLOAT NOT NULL,
            velocidade_vento FLOAT,
            horario_coleta TIMESTAMP NOT NULL
        );
        """
        hook.run(sql)
        print("Tabela tb_clima_brasilia verificada/criada com sucesso.")

    # Tarefa 1 (Extract): Extrai da API REST
    @task
    def extrair_clima_api() -> dict:
        # Coordenadas: Brasilia (Lat: -15.78, Lon: -47.93)
        url = "https://api.open-meteo.com/v1/forecast?latitude=-15.78&longitude=-47.93&current_weather=true"
        print(f"Buscando dados em: {url}")
        
        response = requests.get(url)
        response.raise_for_status() # Verifica se nao deu erro 404/500
        
        dados_json = response.json()
        clima_atual = dados_json['current_weather']
        
        print(f"Dados brutos extraidos: {clima_atual}")
        
        # O RETURN salva automaticamente no XCom!
        return clima_atual

    # Tarefa 2 (Transform): Limpa e prepara
    # Ao colocar o parametro (dados_brutos), o Airflow faz o XCom PULL automaticamente!
    @task
    def transformar_dados(dados_brutos: dict) -> dict:
        temperatura = dados_brutos.get('temperature')
        vento = dados_brutos.get('windspeed')
        
        # Pegamos o horario do proprio servidor que ta rodando o pipeline
        horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dado_transformado = {
            'temp_celsius': float(temperatura),
            'vento_kmh': float(vento),
            'horario_registro': horario
        }
        
        print(f"Dados apos transformacao: {dado_transformado}")
        return dado_transformado

    # Tarefa 3 (Load): Salva no Banco de Dados Postgres
    @task
    def carregar_postgres(dados_prontos: dict):
        # Utiliza o Hook nativo para gerenciar a conexao 'postgres_default'
        hook = PostgresHook(postgres_conn_id='postgres_default')
        
        sql_insert = """
            INSERT INTO tb_clima_brasilia (temperatura, velocidade_vento, horario_coleta)
            VALUES (%s, %s, %s);
        """
        
        # A funcao run() do hook ja abre a conexao, insere e da o commit com seguranca.
        hook.run(sql_insert, parameters=(
            dados_prontos['temp_celsius'],
            dados_prontos['vento_kmh'],
            dados_prontos['horario_registro']
        ))
        
        print(f"Registro inserido no banco de dados com sucesso!")

    # 4. Definicao do Fluxo de Dependencias
    # No Airflow 3 / TaskFlow API, a sequencia eh definida chamando as funcoes
    task_criar = criar_tabela()
    
    # Extrai e guarda o XComArg
    dados_extraidos = extrair_clima_api()
    
    # Transforma recebendo o XComArg (Isso define que Transform depende de Extract)
    dados_limpos = transformar_dados(dados_extraidos)
    
    # Carrega recebendo o XComArg (Load depende de Transform)
    task_carregar = carregar_postgres(dados_limpos)
    
    # Garantimos que a tabela e criada antes de tudo
    task_criar >> dados_extraidos

# Instancia a DAG para que o Airflow a reconheca
dag_instancia = clima_etl_pipeline()
