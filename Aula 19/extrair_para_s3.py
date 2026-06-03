import os
import glob
import boto3

print("--- [Fase 1: EXTRAÇÃO & LANDING] Enviando arquivos brutos de qualidade de água para o S3 ---")

# 1. Localizar arquivos CSV na pasta de dados brutos
# Usamos caminhos relativos em relação ao local do script para maior portabilidade
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados brutos")
files = glob.glob(os.path.join(DADOS_BRUTOS_DIR, "*.csv"))

if not files:
    print(f"Nenhum arquivo CSV encontrado na pasta: {DADOS_BRUTOS_DIR}")
    exit(1)

# Configurações do S3 - Substitua com as suas chaves AWS antes de executar
S3_BUCKET_NAME = 'ibmec-dados-aula19'
AWS_ACCESS_KEY = 'SUA_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'SUA_AWS_SECRET_KEY'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# 2. Upload de cada arquivo para o S3
for file_path in files:
    file_name = os.path.basename(file_path)
    # Substituir espaços por sublinhados para facilitar o uso no Snowflake/S3
    s3_key = f"dados_brutos/{file_name.replace(' ', '_')}"
    
    print(f"Fazendo upload de '{file_name}' para 's3://{S3_BUCKET_NAME}/{s3_key}'...")
    
    try:
        with open(file_path, 'rb') as data:
            s3_client.upload_fileobj(data, S3_BUCKET_NAME, s3_key)
        print(f"Arquivo {file_name} enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar {file_name}: {e}")

print("\nUpload de todos os arquivos concluído!")
