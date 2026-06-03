# airflow_dag_pipeline.py

# 1. Importação das bibliotecas essenciais do Apache Airflow e Python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# 2. Lógica de Execução: Função nativa que será encapsulada pelo PythonOperator
def print_hello():
    """
    Função simples em Python que será executada pelo Worker.
    O retorno (opcional) será registrado nos Logs da interface gráfica.
    """
    mensagem = "Hello World, Airflow!"
    print(mensagem)
    return mensagem

# 3. Definição de argumentos padrão (Default Arguments)
# Boa prática: Evita a repetição de parâmetros idênticos em todas as Tasks
default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 1, # Tentativas automáticas em caso de falha
    'retry_delay': timedelta(minutes=5)
}

# 4. Instanciação do Objeto DAG (O Contêiner Lógico)
# Utiliza-se o 'with' (Context Manager) para associar as Tasks automaticamente a esta DAG
with DAG(
    dag_id='primeiro_hello_world_airflow',
    default_args=default_args,
    description='Pipeline de demonstração para a Aula 19',
    start_date=datetime(2026, 5, 1), # Marco histórico de início [1]
    schedule='@daily',               # Expressão Cron: Execução diária [1]
    catchup=False                    # Impede a execução retroativa do histórico [1]
) as dag:


    # 5. Construção de Tasks - Os Operators
    
    # Task 1: Especializada em comandos do sistema operacional
    tarefa_bash = BashOperator(
        task_id='iniciando_pipeline',
        bash_command='echo "Iniciando Pipeline..."'
    )

    # Task 2: Especializada em rodar métodos nativos da linguagem Python
    tarefa_python = PythonOperator(
        task_id='imprimir_hello_world',
        python_callable=print_hello
    )

    # 6. Orquestração e Dependências Lógicas (Controlando o Fluxo)
    # Garante que a tarefa Python só será iniciada após o sucesso absoluto da tarefa Bash
    tarefa_bash >> tarefa_python