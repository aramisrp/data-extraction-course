# Roteiro de Demonstração Prática (Aula 19)
## Pipeline ELT Completo: Python (Extract) → AWS S3 (Data Lake) → Snowflake (Load) → Airflow & dbt (Transform)

Este guia prático foi desenhado para ser executado ao vivo em sala de aula. Ele demonstra de ponta a ponta como os dados saem de uma origem fictícia, passam pelo armazenamento na nuvem e são transformados no Data Warehouse.

---

## 📋 Pré-requisitos para o Professor

1. **Conta AWS (Gratuita):** Um bucket S3 criado (ex: `ibemec-dados-aula19`).
2. **Chaves AWS IAM:** Um par de chaves `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` com permissão de leitura/escrita no bucket.
3. **Conta Snowflake (Free Trial):** Snowflake oferece 30 dias gratuitos sem precisar de cartão de crédito. Crie a conta na região AWS mais próxima.
4. **Airflow Local Rodando:** O ambiente Docker/Local configurado com as dependências instaladas (`astronomer-cosmos`, etc.).

---

### 🪣 Como Criar o Bucket S3 `ibemec-dados-aula19`

Você pode criar o bucket de duas formas (mostre uma delas aos alunos):

#### Opção A: Pelo Console Web da AWS (Interface Visual)
1. Faça login no Console da AWS e digite **S3** na barra de pesquisa superior.
2. Clique no botão laranja **Create bucket** (Criar bucket).
3. Em **Bucket name** (Nome do bucket), digite: `ibemec-dados-aula19` (os nomes de buckets S3 são globais; se este nome já estiver em uso por outro usuário, mude o sufixo e lembre de atualizar no script Python e na sua DAG).
4. Em **AWS Region** (Região), escolha a mesma região em que seu Snowflake está rodando ou uma próxima (ex: *us-east-1*).
5. Mantenha a opção **Block *all* public access** (Bloquear todo acesso público) ativada.
6. Role até o fim da página e clique em **Create bucket**.

#### Opção B: Via AWS CLI (Linha de Comando)
Se você já tiver o AWS CLI configurado localmente:
```bash
aws s3api create-bucket --bucket ibemec-dados-aula19 --region us-east-1
```

---

## 🛠️ Passo 1: Extração e Carga no S3 (Extract)

Para simular o sistema de origem, criaremos um script simples em Python. Ele simula a extração de um banco transacional e envia o arquivo resultante para o S3.

### Script de Simulação (`extrair_para_s3.py`)

Crie este arquivo na máquina local ou mostre-o no VS Code:

```python
import pandas as pd
import boto3
import io

print("--- [Fase 1: EXTRAÇÃO] Simulando extração de dados transacionais ---")

# 1. Gerar dados simulados (origem)
dados_clientes = {
    'id': [101, 102, 103, 104, 105],
    'nome': ['Ana Silva', 'Bruno Souza', 'Carlos Lima', 'Daniela Oliveira', 'Eduardo Santos'],
    'email': ['ana@email.com', 'bruno@email.com', 'carlos@email.com', 'daniela@email.com', 'eduardo@email.com'],
    'data_cadastro': ['2026-05-20', '2026-05-21', '2026-05-21', '2026-05-21', '2026-05-21']
}
df = pd.DataFrame(dados_clientes)
print("Dados extraídos da origem (Tabela Clientes):")
print(df)

# Convertendo para arquivo CSV em memória (sem salvar no disco local)
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)

# 2. Upload do arquivo bruto para o S3 (Staging Area / Data Lake)
S3_BUCKET_NAME = 'ibemec-dados-aula19' # Substitua pelo seu bucket
AWS_ACCESS_KEY = 'SUA_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'SUA_AWS_SECRET_KEY'

print(f"\n--- [Fase 2: LANDING] Fazendo upload para s3://{S3_BUCKET_NAME}/clientes/clientes.csv ---")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

s3_client.put_object(
    Bucket=S3_BUCKET_NAME,
    Key='clientes/clientes.csv',
    Body=csv_buffer.getvalue()
)

print("Upload concluído com sucesso!")
```

> [!TIP]
> **Dica de Aula:** Mostre aos alunos o console da AWS S3 antes e depois de rodar o script para que vejam o arquivo `clientes.csv` surgir na pasta indicada.

---

## ❄️ Passo 2: Preparação do Snowflake (Load)

### ❄️ Como Criar Conta e Acessar o Console do Snowflake

Para utilizar o Snowflake gratuitamente em sala de aula (com $400 em créditos válidos por 30 dias, sem necessidade de cartão de crédito):

#### 1. Criar a Conta Free Trial
1. Acesse o site oficial de cadastro: [signup.snowflake.com](https://signup.snowflake.com/).
2. Preencha seus dados básicos:
   * **First Name** e **Last Name** (Nome e Sobrenome)
   * **Email** (use seu e-mail de preferência)
   * **Company** (pode colocar "IBEMEC")
   * **Role** (ex: *Educator* ou *Developer*)
   * **Country** (Brasil)
3. Clique em **Continue**.
4. Escolha a Edição do Snowflake:
   * Selecione **Enterprise** (recomendado, pois inclui todos os recursos padrão e analíticos avançados).
5. Escolha o Provedor de Nuvem e Região:
   * **Cloud Provider:** Selecione **Amazon Web Services (AWS)** (para facilitar a integração nativa com nosso bucket S3).
   * **Region:** Selecione a região recomendada ou a mais próxima (ex: *US East (N. Virginia)*).
6. Aceite os termos de serviço e clique em **Get Started**.

#### 2. Ativar a Conta e Definir Senha
1. Acesse a caixa de entrada do seu e-mail cadastrado.
2. Abra o e-mail da Snowflake e clique no botão **Click to Activate** para ativar a sua conta.
3. Defina um **Username** (Nome de usuário) e **Password** (Senha de acesso) seguros.

#### 3. Acessar o Console e Abrir a Worksheet
1. Após criar suas credenciais, você será direcionado para o console principal do Snowflake (conhecido como *Snowsight*).
2. Para criar o espaço onde executará os comandos SQL:
   * No menu lateral esquerdo, clique em **Projects** e depois em **Worksheets**.
   * No canto superior direito, clique no botão azul **+** (ou **+ Worksheet**) e selecione **SQL**.
   * Isso abrirá uma tela com um editor de texto onde você poderá colar e rodar o script SQL a seguir.

### Comandos SQL de Preparação

Abra o console do Snowflake (Worksheet) e execute os comandos abaixo para criar a estrutura que receberá os dados brutos:

```sql
-- 1. Criar o banco de dados brutos
CREATE DATABASE RAW;
CREATE SCHEMA RAW.PUBLIC;

-- 2. Criar a tabela destino correspondente ao arquivo CSV
CREATE OR REPLACE TABLE RAW.PUBLIC.CLIENTES_BRUTOS (
    id INT,
    nome VARCHAR(100),
    email VARCHAR(100),
    data_cadastro DATE
);

-- 3. Testar a carga manualmente (Opcional, pois o Airflow automatizará isso)
COPY INTO RAW.PUBLIC.CLIENTES_BRUTOS
FROM 's3://ibemec-dados-aula19/clientes/'
CREDENTIALS = (AWS_KEY_ID='SUA_AWS_ACCESS_KEY' AWS_SECRET_KEY='SUA_AWS_SECRET_KEY')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);

-- 4. Verificar se os dados foram inseridos
SELECT * FROM RAW.PUBLIC.CLIENTES_BRUTOS;

-- 5. Limpar a tabela para a demonstração do Airflow
TRUNCATE TABLE RAW.PUBLIC.CLIENTES_BRUTOS;
```

---

## 💨 Passo 3: Orquestração no Airflow (Orchestrate & Transform)

Agora que a origem está no S3 e o destino no Snowflake está pronto, configure a automação:

### 1. Configurar a Conexão no Airflow UI
1. Vá em **Admin → Connections → Add a new record**.
2. **Connection Id:** `snowflake_default`
3. **Connection Type:** `Snowflake`
4. **Host / Account:** `seu_id_snowflake.regiao.aws` (o link de acesso sem `https://`)
5. **Schema:** `PUBLIC`
6. **Login:** `SeuUsuario`
7. **Password:** `SuaSenha`
8. **Database:** `RAW`
9. **Warehouse:** `COMPUTE_WH`

### 2. Rodar a DAG
1. Mostre a DAG `aula_19_elt_s3_snowflake_dbt` no painel principal do Airflow.
2. Destaque aos alunos que:
   * A primeira Task executará o comando `COPY INTO` de forma segura.
   * O grupo de tarefas do **dbt Cosmos** varrerá o repositório de SQLs e criará nós independentes para cada modelo (ex: `stg_clientes`, `fct_vendas`, etc.).
3. Ative e dispare a DAG (botão Play).
4. Acompanhe a execução em tempo real na aba **Graph View** ou **Grid View**.

---

## 📊 Passo 4: O "Grand Finale" (Visualização no Snowflake)

Volte para a Worksheet do Snowflake e mostre que os dados brutos foram populados automaticamente pela carga do S3 e, em seguida, as visões analíticas geradas pelo dbt surgiram em outros schemas (ex: `ANALYTICS.dim_clientes`).

```sql
-- Veja que o Airflow preencheu a tabela automaticamente!
SELECT * FROM RAW.PUBLIC.CLIENTES_BRUTOS;
```
