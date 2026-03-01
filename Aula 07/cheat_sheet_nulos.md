# Cheat Sheet: Manipulação de Dados Ausentes com Pandas

Dominar a limpeza de dados ausentes (NaN / nulos) é essencial para qualquer Cientista ou Engenheiro de Dados. Abaixo, resumimos as operações fundamentais que você utilizará como suas ferramentas cirúrgicas no dataset.

## 1. Diagnosticando o Problema

Antes de tratar, é vital inspecionar onde estão os buracos.

```python
import pandas as pd
import seaborn as sns

# Visualizando contagem de nulos por coluna
print(df.isnull().sum())

# Visualizando o percentual de nulos
percentual_nulos = (df.isnull().sum() / len(df)) * 100
print(percentual_nulos)

# Mapa de Calor (Visão Gráfica)
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
```

---

## 2. A "Faca": O Método `.dropna()`

Usado para _deletar_ (amputar) dados indesejados.

### Exclusão de Linhas (Axis 0)

Quando uma linha tem informações críticas faltando, ela geralmente deve ser removida.

```python
# Remove qualquer linha que tenha pelo menos UM valor nulo (drástico)
df.dropna(axis=0, how='any', inplace=True)

# Remove a linha apenas se TODAS as suas colunas forem nulas
df.dropna(axis=0, how='all', inplace=True)

# Remove a linha somente se os valores nulos estiverem em colunas específicas (ex: ID)
df.dropna(subset=['ID_Cliente', 'CPF'], inplace=True)
```

### Exclusão de Colunas (Axis 1)

Quando a coluna em si não possui salvação (ex: 80% dos dados faltantes).

```python
# Remove colunas que sejam 100% nulas
df.dropna(axis=1, how='all', inplace=True)

# Remove colunas retendo apenas aquelas com um mínimo de X linhas NÃO NULAS
limite_aceitavel = len(df) * 0.3 # Ex: mantem colunas que têm pelo menos 30% de integridade
df.dropna(axis=1, thresh=limite_aceitavel, inplace=True)
```

---

## 3. A "Seringa": O Método `.fillna()`

Usado para _preencher_ buracos.

### Preenchimento por Constante (Variáveis Categóricas/Texto)

```python
# Substituindo nulos por um texto específico
df['Categoria'].fillna('Desconhecido', inplace=True)
df['Status'].fillna('Pendente', inplace=True)

# Substituindo nulos numéricos por zero (quando fizer sentido de negócio)
df['Quantidade_Vendas'].fillna(0, inplace=True)
```

### Preenchimento Estatístico Univariado (A mais comum)

Valores numéricos geralmente são preenchidos pela média (dados comportados) ou mediana (imune a outliers extremos).

```python
# 1. Calculando a Média (se não houver outliers extremos)
media = df['Idade'].mean()
df['Idade'].fillna(media, inplace=True)

# 2. Calculando a Mediana (mais seguro e robusto para valores com outliers - ex: Renda, Preços)
mediana = df['Renda'].median()
df['Renda'].fillna(mediana, inplace=True)

# 3. Calculando a Moda (para variáveis categóricas, qual o valor mais repete?)
# Atenção: df.mode() retorna uma série, sempre pegue a [0] em caso de empate
moda = df['Bairro'].mode()[0]
df['Bairro'].fillna(moda, inplace=True)
```

### Preenchimento Dicionário (Múltiplas colunas de uma vez)

Maneira rápida e limpa de indicar um preenchimento padrão diferente para cada coluna:

```python
# Criando dicionário com regras para as colunas
valores_padrao = {
    'Idade': df['Idade'].median(),
    'Bairro': df['Bairro'].mode()[0],
    'Status': 'Pendente'
}

df.fillna(value=valores_padrao, inplace=True)
```

---

**💡 Dica de Ouro:**

> Antes de fazer uma inserção de valor (média/mediana), pergunte a si mesmo: _“O quão distorcido ficará o meu dataset real com essa aproximação empurrada artificialmente?”_
> Se a coluna não for fundamental, evite poluir; dropar a coluna (`dropna`) muitas vezes é a escolha mais limpa analiticamente.
