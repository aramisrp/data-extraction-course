from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
import requests

# Definicao de argumentos padrao
default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# 1. Instanciacao da DAG (Metodo Classico com context manager 'with')
with DAG(
    dag_id='pipeline_etl_clima_classico',
    default_args=default_args,
    description='ETL completo com API externa e Operadores Classicos (Aula 17)',
    start_date=datetime(2026, 5, 10),
    schedule='@daily',
    catchup=False,
    tags=['aula17', 'etl', 'api', 'classico']
) as dag:

    # Tarefa 0: Prepara o banco de dados (Cria tabela se nao existir)
    task_criar_tabela = SQLExecuteQueryOperator(
        task_id='criar_tabela',
        conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS tb_clima_brasilia_classico (
            id SERIAL PRIMARY KEY,
            temperatura FLOAT NOT NULL,
            velocidade_vento FLOAT,
            horario_coleta TIMESTAMP NOT NULL
        );
        """
    )

    # Funcao Python para a Tarefa 1 (Extract)
    def funcao_extrair_clima():
        url = "https://api.open-meteo.com/v1/forecast?latitude=-15.78&longitude=-47.93&current_weather=true"
        print(f"Buscando dados em: {url}")
        
        response = requests.get(url)
        response.raise_for_status() 
        
        dados_json = response.json()
        clima_atual = dados_json['current_weather']
        
        print(f"Dados brutos extraidos: {clima_atual}")
        
        # O RETURN no PythonOperator salva automaticamente no XCom do Airflow
        return clima_atual

    # Tarefa 1 (Extract) - Instanciando o PythonOperator
    task_extrair_clima = PythonOperator(
        task_id='extrair_clima',
        python_callable=funcao_extrair_clima
    )


    # Funcao Python para a Tarefa 2 (Transform)
    # Precisamos do **kwargs para ter acesso ao 'ti' (Task Instance)
    def funcao_transformar_dados(**kwargs):
        ti = kwargs['ti']
        
        # PULL: Busca os dados brutos deixados pela task anterior no banco de dados XCom
        dados_brutos = ti.xcom_pull(task_ids='extrair_clima')
        
        temperatura = dados_brutos.get('temperature')
        vento = dados_brutos.get('windspeed')
        horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dado_transformado = {
            'temp_celsius': float(temperatura),
            'vento_kmh': float(vento),
            'horario_registro': horario
        }
        
        print(f"Dados apos transformacao: {dado_transformado}")
        
        # Faz um novo PUSH (return) para que a task do Postgres possa pegar
        return dado_transformado

    # Tarefa 2 (Transform) - Instanciando o PythonOperator
    task_transformar_dados = PythonOperator(
        task_id='transformar_dados',
        python_callable=funcao_transformar_dados
    )

    # Tarefa 3 (Load): Salva no Banco de Dados Postgres via Operator
    # Utilizamos o Jinja {{ }} para ler do XCom e injetar direto na string SQL
    task_carregar_postgres = SQLExecuteQueryOperator(
        task_id='carregar_postgres',
        conn_id='postgres_default',
        sql="""
            INSERT INTO tb_clima_brasilia_classico (temperatura, velocidade_vento, horario_coleta)
            VALUES (
                {{ ti.xcom_pull(task_ids='transformar_dados')['temp_celsius'] }},
                {{ ti.xcom_pull(task_ids='transformar_dados')['vento_kmh'] }},
                '{{ ti.xcom_pull(task_ids='transformar_dados')['horario_registro'] }}'
            );
        """
    )

    # 4. Definicao do Fluxo de Dependencias Classico (Bitshift operator >>)
    task_criar_tabela >> task_extrair_clima >> task_transformar_dados >> task_carregar_postgres
