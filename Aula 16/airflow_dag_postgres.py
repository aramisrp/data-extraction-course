from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

# Definição de argumentos padrão (Default Arguments)
default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Instanciação do Objeto DAG
with DAG(
    dag_id='pipeline_postgres_producao',
    default_args=default_args,
    description='Demonstração de extração e carga com Banco PostgreSQL',
    start_date=datetime(2026, 5, 1),
    schedule='@daily',
    catchup=False
) as dag:

    # Task 1: Criação da Tabela no Postgres
    # Aqui utilizamos uma conexão de banco relacional cliente-servidor real
    criar_tabela = SQLExecuteQueryOperator(
        task_id='criar_tabela_vendas',
        conn_id='postgres_default', # O aluno precisa criar essa conexão na interface web!
        sql="""
            CREATE TABLE IF NOT EXISTS vendas (
                id SERIAL PRIMARY KEY,
                produto VARCHAR(100) NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    )

    # Task 2: Inserção de Dados no Postgres
    inserir_dados = SQLExecuteQueryOperator(
        task_id='inserir_dados_vendas',
        conn_id='postgres_default',
        sql="""
            INSERT INTO vendas (produto, valor) VALUES 
            ('Notebook Airflow', 4500.00),
            ('Monitor Docker', 1200.50);
        """
    )

    # Task 3: Leitura e Log do Postgres
    ler_dados = SQLExecuteQueryOperator(
        task_id='ler_dados_vendas',
        conn_id='postgres_default',
        sql="SELECT * FROM vendas;",
        show_return_value_in_logs=True # Imprime o resultado do SELECT nos Logs do Airflow
    )

    # Orquestração: Definindo o fluxo (Pipeline)
    criar_tabela >> inserir_dados >> ler_dados
