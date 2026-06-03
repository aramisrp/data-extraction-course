from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta
import requests

default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

@dag(
    dag_id='pipeline_etl_financas_b3_avancado',
    default_args=default_args,
    description='ETL Financeiro com Sensor e Data Quality',
    start_date=datetime(2026, 5, 10),
    schedule='@hourly',
    catchup=False,
    tags=['aula17', 'etl', 'financas', 'b3', 'sensor', 'data_quality']
)
def financas_etl_avancado():
    """
    Pipeline Avancado:
    1. Sensor: Verifica se a API do Yahoo Finance está respondendo (HttpSensor).
    2. Extract: Extrai os dados.
    3. Transform: Limpa os dados.
    4. Data Quality: Verifica se o preco eh valido antes de inserir.
    5. Load: Salva no Postgres.
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

    # Tarefa 1 (Sensor): Aguarda a API estar online
    # Requer criar uma Connection no Airflow chamada 'yahoo_api' 
    # (Conn Type: HTTP, Host: https://query2.finance.yahoo.com)
    sensor_api = HttpSensor(
        task_id='checar_api_yahoo',
        http_conn_id='yahoo_api',
        endpoint='v8/finance/chart/PETR4.SA',
        method='GET',
        headers={'User-Agent': 'Mozilla/5.0'},
        response_check=lambda response: response.status_code == 200,
        poke_interval=60, # Tenta a cada 60 segundos
        timeout=300       # Desiste após 5 minutos
    )

    # Tarefa 2 (Extract)
    @task
    def extrair_preco_acao() -> dict:
        ticker = "PETR4.SA" 
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status() 
        return resposta.json()

    # Tarefa 3 (Transform)
    @task
    def transformar_dados(dados_brutos: dict) -> dict:
        meta_dados = dados_brutos['chart']['result'][0]['meta']
        
        preco_atual = float(meta_dados.get('regularMarketPrice', -1))
        simbolo = meta_dados['symbol']
        moeda = meta_dados['currency']
        
        horario_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            'ativo': simbolo.replace('.SA', ''),
            'preco_brl': preco_atual,
            'moeda': moeda,
            'data_hora': horario_atual
        }

    # Tarefa 4 (Data Quality): Validação de Regra de Negócio
    @task
    def validar_qualidade(dados_limpos: dict) -> dict:
        preco = dados_limpos.get('preco_brl')
        
        if preco is None or preco <= 0:
            raise ValueError(f"DATA QUALITY FAIL: Preço inválido ({preco}) para o ativo {dados_limpos.get('ativo')}. Interrompendo pipeline!")
            
        print("DATA QUALITY PASS: Dados aprovados para carga.")
        return dados_limpos

    # Tarefa 5 (Load)
    @task
    def carregar_banco(dados_validados: dict):
        hook = PostgresHook(postgres_conn_id='postgres_default')
        sql_insert = """
            INSERT INTO tb_cotacao_b3 (ticker, preco_brl, moeda, horario_cotacao)
            VALUES (%s, %s, %s, %s);
        """
        
        hook.run(sql_insert, parameters=(
            dados_validados['ativo'],
            dados_validados['preco_brl'],
            dados_validados['moeda'],
            dados_validados['data_hora']
        ))
        
        print(f"Cotacao validada de R$ {dados_validados['preco_brl']} salva no banco.")

    # Fluxo de Execução
    task_init = criar_tabela()
    
    # O sensor nao retorna dados (XCom), entao usamos o bitshift (>>)
    # para garantir que a extracao so comece se o sensor der OK
    dados_api = extrair_preco_acao()
    sensor_api >> dados_api
    
    # Resto do fluxo dependente (TaskFlow)
    dados_processados = transformar_dados(dados_api)
    dados_validados = validar_qualidade(dados_processados)
    task_load = carregar_banco(dados_validados)
    
    # task_init deve acabar antes da extracao
    task_init >> dados_api

dag_instancia = financas_etl_avancado()
