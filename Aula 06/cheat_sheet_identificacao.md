# Cheat Sheet: Diagnóstico e Visualização de Dados Ausentes

**Aula 06 - Identificando os Buracos**

Antes de tratar dados nulos, é preciso localizá-los, contá-los e entender _por que_ eles faltam. Este guia rápido reúne os comandos essenciais do Pandas e teóricos para a etapa de diagnóstico.

## 1. Identificando Valores Nulos (O Sentinela)

No Pandas, dados ausentes em colunas numéricas ou de texto são padronizados como `NaN` (Not a Number) ou `None`.

```python
import pandas as pd
import numpy as np

# Cria uma máscara booleana (True para onde é nulo, False onde tem dado)
df.isnull() # ou df.isna()

# O inverso: True para onde TEM dado, False onde é nulo
df.notnull()
```

## 2. Quantificando a Fome de Dados

É crucial saber o tamanho do estrago para decidir a melhor abordagem de tratamento (Tema da Aula 07).

```python
# Contagem absoluta: Quantas linhas nulas existem em cada coluna?
print(df.isnull().sum())

# Contagem no dataset inteiro: Quantos nulos no total?
print(df.isnull().sum().sum())

# Proporção: Qual a porcentagem de nulos em cada coluna? (Muito útil!)
percentual = (df.isnull().sum() / len(df)) * 100
print(percentual)

# Somente colunas que possuem nulos
nulos_por_coluna = df.isnull().sum()
print(nulos_por_coluna[nulos_por_coluna > 0])
```

## 3. Isolando o Problema

Como ver apenas as linhas que estão causando problema em uma coluna específica?

```python
# Trazendo todas as linhas onde a coluna 'Idade' está vazia
df_sem_idade = df[df['Idade'].isnull()]

# Trazendo todas as linhas que têm PELO MENOS UM valor nulo em qualquer coluna
df_com_buracos = df[df.isnull().any(axis=1)]
```

---

## 4. Teoria Rápida: Por que o dado sumiu? (Mecanismos de Rubin)

Saber como o dado foi perdido determina se você pode jogar a linha fora, preencher com média ou se precisa de modelos complexos.

🎭 **1. MCAR (Missing Completely at Random - Ausente Completamente ao Acaso)**

- **O que é:** O estagiário derrubou café no servidor e apagou 10% da tabela. A perda não tem padrão cronológico ou lógico.
- **Impacto:** A amostra contínua perfeitamente representativa.
- **Tratamento:** Pode-se excluir as linhas impunemente (Listwise deletion) ou usar Média/Mediana.

🕵️ **2. MAR (Missing at Random - Ausente ao Acaso... dependente de terceiros)**

- **O que é:** A probabilidade do dado faltar depende de _outra_ coluna observada. Ex: Homens (Coluna Sexo) tendem a deixar a coluna "Frequência de ida ao médico" em branco.
- **Impacto:** Ignorar esses nulos vai enviesar as estatísticas (sub-representação).
- **Tratamento:** Imputação avançada (KNN, Regressão) usando outras variáveis para prever a lacuna.

🛑 **3. MNAR (Missing Not at Random - Ausente Não ao Acaso)**

- **O que é:** O pior cenário. A ausência depende do próprio valor omitido. Ex: Pessoas com salários muito altos ou muito baixos se recusam a preencher o campo "Renda". Pacientes terminais não retornam para a pesagem ("Peso").
- **Impacto:** Causa viés severo e estrutural no dado. A média da sua tabela será uma mentira.
- **Tratamento:** Requer modelagem especializada e até coleta profunda de domínio. Quase intratável no Pandas simples.

---

## 5. Visualizando os Nulos (Biblioteca Seaborn)

A melhor forma de apresentar a ausência de dados em relatórios executivos.

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
# Cria um mapa de calor das células nulas (amarelo/claro = nulo, escuro = preenchido)
sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
plt.title('Mapa de Calor de Valores Ausentes')
plt.show()
```
