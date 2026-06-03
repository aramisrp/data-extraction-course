from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests

# Definição de argumentos padrão
default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# -------------------------------------------------------------------
# DICA PARA OS ALUNOS SOBRE AGENDAMENTOS:
# O parâmetro 'schedule' aceita macros do Airflow (como '@hourly', '@daily') 
# ou expressões CRON tradicionais.
# Se você quiser rodar a extração diariamente às 10h da manhã, usaria:
# schedule='0 10 * * *'
#
# Já se quiser rodar de segunda a sexta, de hora em hora, entre 10h e 17h
# (horário de pregão da B3):
# schedule='0 10-17 * * 1-5'
# -------------------------------------------------------------------

with DAG(
    dag_id='pipeline_etl_financas_b3_classico',
    default_args=default_args,
    description='ETL Financeiro consumindo acoes da B3 (PythonOperator Clássico)',
    start_date=datetime(2026, 5, 10),
    schedule='@hourly',
    catchup=False,
    tags=['aula17', 'etl', 'financas', 'b3', 'classico']
) as dag:

    # Tarefa 0: Prepara o banco de dados
    def criar_tabela(**kwargs):
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

    task_init = PythonOperator(
        task_id='criar_tabela',
        python_callable=criar_tabela,
    )

    # Tarefa 1 (Extract): Consome a API do Yahoo Finance
    def extrair_preco_acao(**kwargs):
        ticker = "PETR4.SA" 
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Consultando cotacao em: {url}")
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status() 
        
        dados_json = resposta.json()
        print("Payload complexo recebido com sucesso!")
        
        # Envia os dados para a proxima tarefa via XCom
        kwargs['ti'].xcom_push(key='dados_api_raw', value=dados_json)

    task_extract = PythonOperator(
        task_id='extrair_preco_acao',
        python_callable=extrair_preco_acao,
    )

    # Tarefa 2 (Transform): Navega no JSON aninhado
    def transformar_dados(**kwargs):
        # Puxa os dados brutos da tarefa de extracao
        dados_brutos = kwargs['ti'].xcom_pull(task_ids='extrair_preco_acao', key='dados_api_raw')
        
        meta_dados = dados_brutos['chart']['result'][0]['meta']
        preco_atual = float(meta_dados['regularMarketPrice'])
        simbolo = meta_dados['symbol']
        moeda = meta_dados['currency']
        
        horario_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dado_transformado = {
            'ativo': simbolo.replace('.SA', ''), 
            'preco_brl': preco_atual,
            'moeda': moeda,
            'data_hora': horario_atual
        }
        
        print(f"Dados limpos e prontos para carga: {dado_transformado}")
        
        # Envia os dados limpos para a tarefa de carga
        kwargs['ti'].xcom_push(key='dados_limpos', value=dado_transformado)

    task_transform = PythonOperator(
        task_id='transformar_dados',
        python_callable=transformar_dados,
    )

    # Tarefa 3 (Load): Salva no Banco de Dados
    def carregar_banco(**kwargs):
        # Puxa os dados limpos da tarefa de transformacao
        dados_finais = kwargs['ti'].xcom_pull(task_ids='transformar_dados', key='dados_limpos')
        
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

    task_load = PythonOperator(
        task_id='carregar_banco',
        python_callable=carregar_banco,
    )

    # Define a ordem de execucao (Dependencias)
    task_init >> task_extract >> task_transform >> task_load
