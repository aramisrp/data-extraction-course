from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests

# Definicao de argumentos padrao
default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

@dag(
    dag_id='pipeline_etl_financas_b3',
    default_args=default_args,
    description='ETL Financeiro consumindo acoes da B3 via Yahoo Finance',
    start_date=datetime(2026, 5, 10),
    schedule='@hourly',
    catchup=False,
    tags=['aula17', 'etl', 'financas', 'b3']
)
def financas_etl_pipeline():
    """
    Pipeline de Dados Financeiros (ETL)
    1. Extrai o preco atual de uma acao da B3 (ex: PETR4) via API do Yahoo Finance.
    2. Transforma os dados (navega no JSON complexo e extrai o preco).
    3. Carrega no Postgres.
    """

    # Tarefa 0: Prepara o banco de dados
    @task
    def criar_tabela():
        hook = PostgresHook(postgres_conn_id='postgres_default')
        sql = """
        CREATE TABLE IF NOT EXISTS tb_cotacao_b3 (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(20) NOT NULL,
            preco_brl FLOAT NOT NULL,
            moeda VARCHAR(10),
            horario_cotacao TIMESTAMP NOT NULL
        );
        """
        hook.run(sql)
        print("Tabela tb_cotacao_b3 verificada/criada com sucesso.")

    # Tarefa 1 (Extract): Consome a API do Yahoo Finance
    @task
    def extrair_preco_acao() -> dict:
        # Acoes da B3 no Yahoo Finance tem o sufixo '.SA' (Sao Paulo)
        ticker = "PETR4.SA" 
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        
        # O Yahoo Finance bloqueia robos sem User-Agent, entao fingimos ser um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Consultando cotacao em: {url}")
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status() 
        
        dados_json = resposta.json()
        print("Payload complexo recebido com sucesso!")
        
        return dados_json

    # Tarefa 2 (Transform): Navega no JSON aninhado
    @task
    def transformar_dados(dados_brutos: dict) -> dict:
        # O JSON do Yahoo Finance tem varias camadas de listas e dicionarios.
        # Precisamos navegar ate: chart -> result -> [0] -> meta -> regularMarketPrice
        meta_dados = dados_brutos['chart']['result'][0]['meta']
        
        preco_atual = float(meta_dados['regularMarketPrice'])
        simbolo = meta_dados['symbol']
        moeda = meta_dados['currency'] # BRL
        
        horario_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dado_transformado = {
            'ativo': simbolo.replace('.SA', ''), # Remove o .SA para ficar mais limpo (PETR4)
            'preco_brl': preco_atual,
            'moeda': moeda,
            'data_hora': horario_atual
        }
        
        print(f"Dados limpos e prontos para carga: {dado_transformado}")
        return dado_transformado

    # Tarefa 3 (Load): Salva no Banco de Dados
    @task
    def carregar_banco(dados_finais: dict):
        hook = PostgresHook(postgres_conn_id='postgres_default')
        
        sql_insert = """
            INSERT INTO tb_cotacao_b3 (ticker, preco_brl, moeda, horario_cotacao)
            VALUES (%s, %s, %s, %s);
        """
        
        hook.run(sql_insert, parameters=(
            dados_finais['ativo'],
            dados_finais['preco_brl'],
            dados_finais['moeda'],
            dados_finais['data_hora']
        ))
        
        print(f"Cotacao da {dados_finais['ativo']} a R$ {dados_finais['preco_brl']} inserida no BD!")

    # Fluxo de Execucao (TaskFlow API)
    task_init = criar_tabela()
    dados_api = extrair_preco_acao()
    dados_processados = transformar_dados(dados_api)
    task_load = carregar_banco(dados_processados)
    
    # Define a ordem de precedencia (Tabela deve existir antes de extrair)
    task_init >> dados_api

# Registra a DAG
dag_instancia = financas_etl_pipeline()
