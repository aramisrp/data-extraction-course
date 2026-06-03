import duckdb
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt

# Caminho do Data Lake
DATALAKE_RAW = 'data_lake/raw/reddit'

print("="*60)
print("  PROCESSAMENTO BATCH E ARQUITETURA MEDALHÃO COM DUCKDB")
print("="*60)

# Verificar se existem arquivos no Data Lake
arquivos = glob.glob(f"{DATALAKE_RAW}/**/*.parquet", recursive=True)
if not arquivos:
    print(f"[ERRO] Nenhum arquivo Parquet encontrado em '{DATALAKE_RAW}'.")
    print("Por favor, execute primeiro o 'producer.py' e o 'consumer.py' para popular o Data Lake.")
    exit(1)

print(f"[OK] Encontrados {len(arquivos)} arquivos Parquet no Data Lake raw.")

# Conectar a um banco DuckDB persistente local
db_path = 'reddit_analytics.db'
if os.path.exists(db_path):
    os.remove(db_path) # Reinicia o banco para demonstração limpa

con = duckdb.connect(db_path)

# ----------------------------------------------------
# 1. ANÁLISE DE SENTIMENTOS - DEFINIÇÃO DA UDF
# ----------------------------------------------------
def analisar_sentimento_pt(texto):
    """Retorna o sentimento predominante do comentário (Positivo, Negativo ou Neutro)"""
    texto = str(texto).lower()
    palavras_positivas = ['bom', 'boa', 'ótimo', 'otimo', 'excelente', 'maravilhoso', 'gosto', 'gostei', 'legal', 'parabéns', 'sensacional']
    palavras_negativas = ['ruim', 'péssimo', 'pessimo', 'horrível', 'horrivel', 'odeio', 'triste', 'erro', 'errado', 'pior', 'bosta', 'merda', 'lixo']
    
    score = 0
    for p in palavras_positivas:
        score += texto.count(p)
    for p in palavras_negativas:
        score -= texto.count(p)
        
    if score > 0:
        return 'Positivo'
    elif score < 0:
        return 'Negativo'
    else:
        return 'Neutro'

# Registrando a função Python como UDF no DuckDB para que possamos usá-la direto nas consultas SQL
con.create_function("analisar_sentimento_sql", analisar_sentimento_pt, ['VARCHAR'], 'VARCHAR')

# ----------------------------------------------------
# 2. CAMADA BRONZE (Leitura Direta dos Arquivos Brutos)
# ----------------------------------------------------
print("\n[BRONZE] Mapeando arquivos Parquet para a View Bronze...")
# O parâmetro hive_partitioning=True instrui o DuckDB a ler ano, mes, dia do caminho das pastas automaticamente!
con.execute(f"""
    CREATE OR REPLACE VIEW bronze_reddit AS 
    SELECT * FROM read_parquet('{DATALAKE_RAW}/**/*.parquet', hive_partitioning=True);
""")

total_bronze = con.execute("SELECT COUNT(*) FROM bronze_reddit").fetchone()[0]
print(f"[OK] View BRONZE criada. Registros brutos encontrados: {total_bronze}")

# ----------------------------------------------------
# 3. CAMADA SILVER (Limpeza, Deduplicação e Enriquecimento)
# ----------------------------------------------------
print("\n[SILVER] Executando transformações e gerando a Tabela Silver...")
# Deduplicamos por ID escolhendo o registro com a data de ingestão mais recente
con.execute("""
    CREATE OR REPLACE TABLE silver_reddit AS
    WITH deduplicado AS (
        SELECT 
            id,
            author,
            subreddit,
            body,
            epoch_ms(CAST(created_utc * 1000 AS BIGINT)) as created_at,
            ingestion_timestamp,
            ano,
            mes,
            dia,
            ROW_NUMBER() OVER (PARTITION BY id ORDER BY ingestion_timestamp DESC) as rn
        FROM bronze_reddit
    )
    SELECT 
        id,
        author,
        subreddit,
        body,
        created_at,
        ingestion_timestamp,
        ano,
        mes,
        dia,
        -- Chamando nossa UDF Python diretamente no SQL
        analisar_sentimento_sql(body) as sentiment,
        length(body) as body_length
    FROM deduplicado
    WHERE rn = 1;
""")

total_silver = con.execute("SELECT COUNT(*) FROM silver_reddit").fetchone()[0]
print(f"[OK] Tabela SILVER criada (Deduplicada e Enriquecida). Registros limpos: {total_silver}")

# ----------------------------------------------------
# 4. CAMADA GOLD (Agregações para Análise de Negócio)
# ----------------------------------------------------
print("\n[GOLD] Gerando visões agregadas de negócio...")

# Agregação 1: Sentimento Geral
print("\n---> Distribuição de Sentimento:")
df_sentimento = con.execute("""
    SELECT 
        sentiment as "Sentimento", 
        COUNT(*) as "Total",
        round(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM silver_reddit), 2) as "Percentual (%)"
    FROM silver_reddit
    GROUP BY sentiment
    ORDER BY Total DESC;
""").df()
print(df_sentimento.to_string(index=False))

# Agregação 2: Atividade por Hora
print("\n---> Volume de Comentários por Hora do Dia:")
df_horas = con.execute("""
    SELECT 
        strftime(created_at, '%H') as "Hora", 
        COUNT(*) as "Total_Comentarios"
    FROM silver_reddit
    GROUP BY strftime(created_at, '%H')
    ORDER BY "Hora" ASC;
""").df()
print(df_horas.to_string(index=False))

# Agregação 3: Autores Mais Influentes / Ativos e seus Sentimentos
print("\n---> Perfil de Sentimento dos Autores Mais Ativos:")
df_autores = con.execute("""
    SELECT 
        author as "Autor",
        COUNT(*) as "Total_Comentarios",
        COUNT(CASE WHEN sentiment = 'Positivo' THEN 1 END) as "Positivos",
        COUNT(CASE WHEN sentiment = 'Negativo' THEN 1 END) as "Negativos",
        COUNT(CASE WHEN sentiment = 'Neutro' THEN 1 END) as "Neutros"
    FROM silver_reddit
    WHERE author != '[deleted]'
    GROUP BY author
    HAVING COUNT(*) > 1
    ORDER BY Total_Comentarios DESC
    LIMIT 10;
""").df()

if df_autores.empty:
    # Fallback se ninguém comentou mais de uma vez na amostra curta
    df_autores = con.execute("""
        SELECT 
            author as "Autor",
            COUNT(*) as "Total_Comentarios",
            COUNT(CASE WHEN sentiment = 'Positivo' THEN 1 END) as "Positivos",
            COUNT(CASE WHEN sentiment = 'Negativo' THEN 1 END) as "Negativos"
        FROM silver_reddit
        WHERE author != '[deleted]'
        GROUP BY author
        ORDER BY Total_Comentarios DESC
        LIMIT 10;
    """).df()
print(df_autores.to_string(index=False))

# ----------------------------------------------------
# 5. GRAVAR TABELAS DE VOLTA NO LAKE COMO PARQUET GOLD/SILVER
# ----------------------------------------------------
print("\n[LAKEHOUSE] Exportando dados refinados de volta ao Data Lake...")
os.makedirs("data_lake/silver", exist_ok=True)
os.makedirs("data_lake/gold", exist_ok=True)

con.execute("COPY silver_reddit TO 'data_lake/silver/reddit_cleaned.parquet' (FORMAT PARQUET);")
con.execute("COPY (SELECT * FROM silver_reddit GROUP BY ALL) TO 'data_lake/gold/reddit_sentiment_summary.parquet' (FORMAT PARQUET);")
print("[OK] Exportações concluídas! Arquivos criados na pasta 'data_lake/silver' e 'data_lake/gold'.")

# Fechar conexão com o DuckDB
con.close()

# ----------------------------------------------------
# 6. GERAÇÃO DE RELATÓRIO GRÁFICO (MATPLOTLIB)
# ----------------------------------------------------
print("\n[VIZ] Salvando gráfico de análise de sentimento...")
plt.figure(figsize=(10, 5))
colors = ['#95a5a6' if s == 'Neutro' else '#2ecc71' if s == 'Positivo' else '#e74c3c' for s in df_sentimento['Sentimento']]
plt.bar(df_sentimento['Sentimento'], df_sentimento['Total'], color=colors, edgecolor='black', alpha=0.8)
plt.title('Distribuição de Sentimentos dos Comentários no r/brasil', fontsize=14, pad=15)
plt.xlabel('Sentimento', fontsize=12)
plt.ylabel('Quantidade de Comentários', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)

output_img = 'analise_sentimento_reddit.png'
plt.savefig(output_img, bbox_inches='tight', dpi=150)
print(f"[OK] Gráfico salvo como '{output_img}' com sucesso!")
print("\nProcessamento Concluido com Sucesso! [OK]")
print("="*60)
