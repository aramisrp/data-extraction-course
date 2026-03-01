# Plano de Aula 06 - Dados Ausentes: Identificação e Mecanismos

**Disciplina:** Extração e Preparação de Dados (IBM8915)
**Professor:** Luís Aramis
**Data:** 03/03 (Terça-feira)
**Carga Horária:** 2 tempos de 50 minutos (100 min)
**Tópico:** Identificação de valores nulos e compreensão dos mecanismos de ausência.

---

## 1. Objetivos da Aula

### Objetivo Geral

Capacitar os alunos a diagnosticar profundamente a completude de um dataset, compreendendo as razões por trás da falta de dados e aplicando técnicas para mapear e visualizar essas ocorrências.

### Objetivos Específicos

- **Conceitual:** Compreender e diferenciar os mecanismos de ausência de dados: MCAR (Ausente Completamente ao Acaso), MAR (Ausente ao Acaso) e MNAR (Ausente Não ao Acaso).
- **Técnico:** Entender o conceito de _valores de sentinela_ na linguagem Python (como `NaN` e `None`).
- **Prático/Analítico:** Mapear e quantificar a ocorrência de valores nulos em um dataset usando o Pandas e gerar visualizações que destaquem esses "buracos".

---

## 2. Conteúdo Programático

1.  **A Natureza dos Dados Ausentes:**
    - O impacto da omissão de dados em análises estatísticas e modelos de Machine Learning.
    - Como o Pandas representa dados ausentes (valor sentinela `NaN` - _Not a Number_ para floats, `None` para objetos).
2.  **Mecanismos de Ausência (Teoria de Rubin):**
    - **MCAR (Missing Completely at Random):** A probabilidade de o dado faltar não tem relação com nenhuma outra variável.
    - **MAR (Missing at Random):** A probabilidade de o dado faltar tem relação com alguma outra variável observada no dataset.
    - **MNAR (Missing Not at Random):** A probabilidade de o dado faltar depende do próprio valor que está faltando (ex: pessoas com salários mais altos tendem a não revelar seus salários).
3.  **Identificação e Quantificação (Pandas):**
    - Uso de métodos embutidos do Pandas para filtragem e detecção: `isnull()` e `notnull()`.
    - Agregação de nulos: `df.isnull().sum()` e cálculo do percentual de ausência (`df.isnull().sum() / len(df)`).
4.  **Visualização Básica de Nulos:**
    - Técnicas e bibliotecas para plotar matrizes e barras de completude (ex: `missingno` ou gráficos de barras do próprio pandas/matplotlib).

---

## 3. Metodologia e Recursos

- **Metodologia:** Aula expositiva dialogada no primeiro tempo, focada nos conceitos estatísticos (MCAR, MAR, MNAR), seguida de laboratório prático (_live coding_ e resolução de exercícios) no segundo tempo.
- **Recursos:** Projetor multimídia, Jupyter Notebook, Bibliotecas Python (Pandas para manipulação, Matplotlib/Seaborn/Missingno para visualização).

---

## 4. Cronograma Detalhado (100 min)

### Primeiro Tempo: Teoria e Mecanismos (50 min)

| Tempo      | Atividade                    | Detalhamento do Conteúdo                                                                                                                                                                                          | Fonte |
| :--------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---- |
| **10 min** | **Contextualização**         | Retomada do Dicionário de Dados construído na Aula 05. Introdução ao problema: "Descobrimos buracos nos dados na aula passada. Mas por que eles estão lá?".                                                       |       |
| **25 min** | **Teoria: MCAR, MAR e MNAR** | Explicação profunda dos 3 mecanismos usando exemplos da vida real (ex: dados médicos de saúde ou pesquisas de censo). Discussão: Por que identificar o mecanismo define como vamos tratar o erro na próxima aula? |       |
| **15 min** | **O Sentinela em Python**    | Apresentação do `NaN` da biblioteca NumPy. Explicar como o Pandas exclui automaticamente os valores `NaN` ao calcular estatísticas descritivas (ex: média).                                                       |       |

### Segundo Tempo: Laboratório Prático e Visualização (50 min)

| Tempo      | Atividade                    | Detalhamento do Conteúdo                                                                                                                                                                                 | Fonte |
| :--------- | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---- |
| **15 min** | **Mão na Massa: Mapeamento** | _Live coding_ com os comandos de diagnóstico de nulos. Execução de `df.isnull().sum()` e criação de uma máscara booleana para encontrar os registros esburacados.                                        |       |
| **25 min** | **Prática de Visualização**  | Início do notebook `lab_04_missing_values_viz.ipynb`. Os alunos carregarão um dataset defeituoso e deverão criar um gráfico de barras ordenado mostrando o percentual de dados faltantes de cada coluna. |       |
| **10 min** | **Fechamento e Portfólio**   | Orientações finais sobre a entrega do notebook. Preparação para a próxima aula (Aula 07), onde será iniciada a imputação univariada para preencher os buracos encontrados hoje.                          |       |

---

## 5. Avaliação e Entrega (Atividade Portfólio)

Conforme as diretrizes institucionais, a avaliação formativa será vinculada ao repositório GitHub do aluno:

- **Entrega:** Notebook `lab_04_missing_values_viz.ipynb` commitado no repositório `data-extraction-course`.
- **Critérios:** O aluno deve demonstrar que conseguiu carregar os dados, extrair o quantitativo exato e o percentual de valores nulos por coluna, e gerar uma visualização em formato de gráfico que escancare o grau de ausência de informações do dataset.

---

## 6. Referências Bibliográficas

- **Plano de Ensino e Cronograma da Disciplina.**
- **McKinney, Wes.** _Python para Análise de Dados_. Novatec. (Capítulo 7: Limpeza e preparação dos dados - Seção 7.1 Tratando dados ausentes e valores sentinela).
