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
    dag_id='pipeline_sqlite_introducao',
    default_args=default_args,
    description='Demonstração de extração e carga com SQLite nativo',
    start_date=datetime(2026, 5, 1),
    schedule='@daily',
    catchup=False
) as dag:

    # Task 1: Criação da Tabela (DDL)
    # conn_id="sqlite_default" aponta para a conexão pré-configurada no Airflow
    criar_tabela = SQLExecuteQueryOperator(
        task_id='criar_tabela_usuarios',
        conn_id='sqlite_default',
        sql="""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    )

    # Task 2: Inserção de Dados (DML)
    inserir_dados = SQLExecuteQueryOperator(
        task_id='inserir_dados_teste',
        conn_id='sqlite_default',
        sql="""
            INSERT INTO usuarios (nome) VALUES 
            ('João da Silva'),
            ('Maria Souza');
        """
    )

    # Task 3: Leitura e Log (DQL)
    ler_dados = SQLExecuteQueryOperator(
        task_id='ler_dados_inseridos',
        conn_id='sqlite_default',
        sql="SELECT * FROM usuarios;",
        show_return_value_in_logs=True # Exibe o resultado do SELECT nos Logs do Airflow
    )

    # Orquestração: Definindo a ordem de execução
    criar_tabela >> inserir_dados >> ler_dados
