from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import pandas as pd
import os

default_args = {
    'owner': 'aluno_ibm8915',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

@dag(
    dag_id='pipeline_etl_csv_sensor_dq',
    default_args=default_args,
    description='PBL Aula 18: FileSensor e Data Quality em CSV',
    start_date=datetime(2026, 5, 10),
    schedule='@daily',
    catchup=False,
    tags=['aula18', 'etl', 'csv', 'sensor', 'data_quality']
)
def csv_etl_avancado():
    
    # Caminho do arquivo esperado pelo negócio
    ARQUIVO_CSV = '/tmp/dados_vendas.csv'
    
    # ---------------------------------------------------------
    # 1. Inserir um Sensor aguardando o CSV
    # ---------------------------------------------------------
    # O FileSensor checa a existência do arquivo na máquina/container
    aguardando_csv = FileSensor(
        task_id='esperar_arquivo_csv',
        filepath=ARQUIVO_CSV,
        poke_interval=30, # Checa a cada 30 segundos se o arquivo chegou
        timeout=300,      # Desiste (Fail) após 5 minutos esperando
        mode='poke'
    )

    # ---------------------------------------------------------
    # 2. Ler o CSV e contar os nulos
    # 3. Levantar erro se a coluna crítica estiver 100% nula
    # ---------------------------------------------------------
    @task
    def validar_qualidade_csv(caminho_arquivo: str):
        print(f"Lendo o arquivo: {caminho_arquivo}")
        
        # Lê o CSV usando pandas
        df = pd.read_csv(caminho_arquivo)
        
        # Coluna crítica para o negócio (exemplo: 'valor_venda')
        coluna_critica = 'valor_venda'
        
        # Segurança: Verifica se a coluna de fato existe no CSV
        if coluna_critica not in df.columns:
            raise ValueError(f"DATA QUALITY FAIL: A coluna '{coluna_critica}' esperada não veio no arquivo!")
        
        # Lógica de contagem
        total_linhas = len(df)
        nulos_coluna_critica = df[coluna_critica].isnull().sum()
        
        print(f"Total de linhas no CSV: {total_linhas}")
        print(f"Linhas com '{coluna_critica}' NULA: {nulos_coluna_critica}")
        
        # A Regra de Negócio: Barrar (Fail) se 100% for nulo
        if total_linhas > 0 and nulos_coluna_critica == total_linhas:
            raise ValueError(f"DATA QUALITY FAIL: A coluna '{coluna_critica}' está 100% vazia! O Data Warehouse não pode receber isso. Interrompendo pipeline!")
            
        print("DATA QUALITY PASS: Dados aprovados com sucesso no Gatekeeper!")
        
        # Passa metadados para a próxima task via XCom (evitar passar o DataFrame inteiro se for muito grande)
        return {
            'total_linhas': total_linhas,
            'linhas_validas': int(total_linhas - nulos_coluna_critica)
        }
        
    @task
    def carregar_dados(metricas: dict):
        print(f"Iniciando carga de {metricas['linhas_validas']} linhas válidas no banco de dados (Data Warehouse)...")
        # A lógica real de carga SQL entraria aqui (ex: to_sql para o Postgres)
        print("Carga finalizada com sucesso!")

    # ---------------------------------------------------------
    # Orquestração (Definindo a ordem)
    # ---------------------------------------------------------
    # A validação e leitura do CSV só começa SE (>>) o sensor confirmar a chegada
    validacao = validar_qualidade_csv(ARQUIVO_CSV)
    
    aguardando_csv >> validacao >> carregar_dados(validacao)

# Instancia a DAG
dag_instancia = csv_etl_avancado()
