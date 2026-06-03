from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.empty import EmptyOperator

# Importando a biblioteca Cosmos para renderizar o dbt como DAG
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

# 1. Configuracoes do dbt Cosmos
# Informamos onde o projeto dbt esta localizado e como o Cosmos deve se conectar
DBT_PROJECT_PATH = "/opt/airflow/dags/dbt_project_WQ" # Caminho no container do Airflow

profile_config = ProfileConfig(
    profile_name="meu_perfil_snowflake",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_default", # A mesma connection cadastrada na UI do Airflow
        profile_args={"database": "RAW", "schema": "PUBLIC"},
    )
)

# 2. Argumentos padroes da DAG
default_args = {
    'owner': 'engenharia_dados',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 23),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 3. Definicao da DAG
with DAG(
    'aula_19_elt_s3_snowflake_dbt',
    default_args=default_args,
    description='DAG ELT orquestrando carga do S3 para Snowflake e transformacao via dbt Cosmos',
    schedule='@daily',
    catchup=False,
    tags=['aula_19', 'MDS', 'ELT', 'dbt', 'Snowflake'],
) as dag:

    # Task 0 Inicial
    start = EmptyOperator(task_id='start')

    # Task 1: LOAD (Carregar dados brutos do S3 para o Snowflake)
    # Aqui utilizamos o poder do Data Warehouse nativamente (COPY INTO)
    # A extracao para o S3 ja aconteceu previamente (via script 'extrair_para_s3.py').
    # E o arquivo foi salvo no formato CSV com delimitador ponto e virgula (;).

    load_s3_to_snowflake = SQLExecuteQueryOperator(
        task_id='carregar_dados_s3_para_snowflake',
        conn_id='snowflake_default',
        sql="""
            COPY INTO RAW.PUBLIC.QUALIDADE_AGUA_BRUTA
            FROM 's3://larp-dados-aula19/dados_brutos/'
            CREDENTIALS = (AWS_KEY_ID='SEU_AWS_ACCESS_KEY' AWS_SECRET_KEY='SEU_AWS_SECRET_KEY')
            FILE_FORMAT = (
                TYPE = CSV 
                FIELD_DELIMITER = ';' 
                SKIP_HEADER = 1 
                ENCODING = 'iso-8859-1'
            )
            PATTERN = '.*\\.csv';
        """,
        doc_md="Carrega os arquivos CSV de qualidade de água do bucket S3 diretamente para a tabela bruta do Snowflake."
    )

    # Task 2: TRANSFORM (dbt)
    # O DbtTaskGroup do Cosmos varre a pasta dbt_project_example e cria 
    # uma task individual para CADA arquivo .sql (modelo) ou teste que encontrar.
    dbt_transform = DbtTaskGroup(
        group_id="transformacoes_dbt",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        execution_config=ExecutionConfig(dbt_executable_path="/usr/local/bin/dbt"),
        operator_args={"install_deps": True}
    )

    # Task 3 Final
    end = EmptyOperator(task_id='end')

    # 4. Ordem de Execucao (Dependencias)
    start >> load_s3_to_snowflake >> dbt_transform >> end
