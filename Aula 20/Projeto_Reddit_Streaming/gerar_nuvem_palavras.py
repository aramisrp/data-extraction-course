import pandas as pd
import glob
import os
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Baixa o dicionário de stopwords do NLTK (silenciosamente)
nltk.download('stopwords', quiet=True)

print("Buscando dados no Data Lake (arquivos Parquet)...")

# Procurar todos os arquivos parquet no data lake local, em qualquer subdiretório de data
arquivos_parquet = glob.glob('data_lake/raw/reddit/**/*.parquet', recursive=True)

if not arquivos_parquet:
    print("Nenhum arquivo Parquet encontrado. Certifique-se de que o Consumidor já rodou e salvou dados.")
    exit()

# Ler todos os arquivos para um único DataFrame do Pandas
df_list = [pd.read_parquet(arq) for arq in arquivos_parquet]
df = pd.concat(df_list, ignore_index=True)

print(f"Total de registros (comentários) carregados: {len(df)}")

if 'body' not in df.columns:
    print("Coluna 'body' não encontrada nos dados.")
    exit()

print("Realizando limpeza dos dados textuais (NLP)...")
def limpar_texto(texto):
    # Converte para minúsculas
    texto = str(texto).lower()
    # Remove links/URLs
    texto = re.sub(r'http\S+|www\.\S+', '', texto)
    # Remove marcações do reddit como /u/usuario e r/comunidade
    texto = re.sub(r'/?u/\w+', '', texto)
    texto = re.sub(r'/?r/\w+', '', texto)
    # Remove números, pontuações e caracteres especiais, mantendo letras com acento do Português
    texto = re.sub(r'[^a-záàâãéèêíïóôõöúçñ ]', ' ', texto)
    # Remove espaços duplos ou múltiplos gerados pelas remoções anteriores
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

# Aplica a função de limpeza em todos os comentários processados
df['body_limpo'] = df['body'].dropna().apply(limpar_texto)

# Juntar todo o texto limpo para a nuvem
texto_completo = " ".join(df['body_limpo'].tolist())

# Configurar stopwords avançadas com NLTK (pronomes, artigos, preposições, conjunções, etc)
stopwords_pt = set(stopwords.words('portuguese'))
# Adicionamos também gírias e abreviações típicas de redes sociais
stopwords_pt.update(['ter','cara','todo','vai','pra', 'pro', 'tá', 'to', 'vc', 'vcs', 'q', 'pq', 'nao', 'sim', 'aí', 'lá', 'aqui', 'sobre', 'tem', 'já', 'tudo', 'muito'])

print("Processando textos e gerando Nuvem de Palavras...")

# Gerar a nuvem de palavras
wordcloud = WordCloud(
    width=1000, 
    height=500, 
    background_color='white',
    colormap='inferno', # Um esquema de cores impactante
    stopwords=stopwords_pt,
    max_words=150
).generate(texto_completo)

# Plotar a imagem usando Matplotlib
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Esconder os eixos
plt.title(f"Nuvem de Palavras do r/brasil (Baseado em {len(df)} comentários)", fontsize=18, pad=20)

# Salvar a imagem localmente e também exibir na tela
output_file = 'nuvem_palavras_reddit.png'
plt.savefig(output_file, bbox_inches='tight')
print(f"Imagem gerada e salva com sucesso como: {output_file}")

# Abre a janela gráfica
plt.show()
