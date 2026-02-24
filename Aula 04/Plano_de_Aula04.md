# Plano de Aula 04 - Análise Exploratória: Variáveis Numéricas e Categóricas

**Disciplina:** Extração e Preparação de Dados (IBM8915)
**Professor:** Luís Aramis
**Data:** 24/02 (Terça-feira)
**Carga Horária:** 2 tempos de 50 minutos (100 min)
**Tópico:** Classificação de variáveis e estatística descritiva com Pandas.

---

## 1. Objetivos da Aula

### Objetivo Geral
Capacitar os alunos a realizar a Análise Exploratória de Dados (EDA - *Exploratory Data Analysis*) inicial, com foco na diferenciação e tratamento estatístico básico de variáveis numéricas e categóricas.

### Objetivos Específicos
*   **Conceitual:** Diferenciar variáveis Numéricas (Contínuas e Discretas) de Categóricas (Nominais e Ordinais).
*   **Prático (Pandas):** Utilizar `dtypes` para identificar tipos de dados no Pandas e converter tipos incorretos.
*   **Analítico:** Aplicar estatísticas descritivas apropriadas para cada tipo de variável (média/desvio padrão para numéricas; frequência/moda para categóricas).
*   **Técnico:** Introduzir o tipo de dado `category` do Pandas para otimização de memória e semântica.

---

## 2. Conteúdo Programático

1.  **Revisão:** Acesso aos dados (carregados via CSV ou SQL nas aulas anteriores).
2.  **Taxonomia dos Dados:**
    *   Variáveis Numéricas: Contínuas vs. Discretas.
    *   Variáveis Categóricas: Nominais vs. Ordinais.
3.  **Inspeção Inicial no Pandas:**
    *   Uso de `.info()`, `.head()` e `.dtypes`.
4.  **Análise de Variáveis Numéricas:**
    *   Medidas de tendência central (média, mediana) e dispersão (desvio padrão, quartis),.
    *   O método `.describe()`.
5.  **Análise de Variáveis Categóricas:**
    *   Tabelas de frequência com `.value_counts()`.
    *   Cardinalidade e valores únicos (`.unique()`, `.nunique()`).
    *   O tipo `Categorical` do Pandas.

---

## 3. Metodologia e Recursos

*   **Metodologia:** Estudo de caso utilizando um dataset real (sugestão: dados do *Titanic* ou *Gorjetas/Tips* mencionados nas fontes,). A aula alternará entre exposição teórica breve e *live coding* no Jupyter Notebook.
*   **Recursos:** Projetor, Quadro Branco, Jupyter Notebook, Bibliotecas Python (Pandas, NumPy).

---

## 4. Cronograma Detalhado (100 min)

### Primeiro Tempo: Identificação e Tipagem (50 min)

| Tempo | Atividade | Detalhamento do Conteúdo | Fonte de Apoio |
| :--- | :--- | :--- | :--- |
| **10 min** | **Check-in e Contexto** | Conectar com a aula anterior (SQL). Explicar que após extrair ("SELECT"), precisamos entender o que temos ("EDA"). Apresentação do *Estudo de Caso* do dia. |, |
| **15 min** | **Teoria: Tipos de Variáveis** | Exposição dialogada sobre a taxonomia dos dados. <br>• **Numérica:** Idade (discreta), Salário (contínua). <br>• **Categórica:** Gênero (nominal), Escolaridade (ordinal). |, |
| **15 min** | **Prática: Inspeção Inicial** | Carregamento do dataset. Uso de `df.info()` para ver nulos e tipos. Uso de `df.dtypes`. Discussão: "O que acontece quando um número é lido como texto (object)?" |, |
| **10 min** | **Prática: Conversão de Tipos** | Correção de tipos de dados. Transformar strings em datas (`to_datetime`) ou números (`to_numeric`). Introdução breve ao tipo `category` para economia de memória. |, |

### Segundo Tempo: Estatística Descritiva (50 min)

| Tempo | Atividade | Detalhamento do Conteúdo | Fonte de Apoio |
| :--- | :--- | :--- | :--- |
| **15 min** | **Explorando Numéricas** | Foco no método `.describe()` para resumo estatístico. Cálculo individual de `.mean()`, `.median()`, `.std()`, `.min()`, `.max()`. Interpretação de quartis (25%, 50%, 75%) para entender distribuição. |,, |
| **15 min** | **Explorando Categóricas** | Como resumir texto? Uso de `.value_counts()` para ver frequências absolutas e relativas (`normalize=True`). Uso de `.unique()` para ver valores distintos. Identificação de inconsistências básicas (ex: "SP" vs "S. Paulo"). |, |
| **10 min** | **Análise Multivariada Simples** | Introdução rápida ao cruzamento de dados. Usar `groupby()` simples: "Qual a média de idade (numérica) por gênero (categórica)?" |, |
| **10 min** | **Encerramento e Portfolio** | Revisão dos principais comandos. Explicação da atividade de portfólio `lab_03_eda_basics.ipynb` que os alunos devem entregar. | |

---

## 5. Avaliação e Entrega

A avaliação será baseada na realização da **Atividade Portfólio (GitHub)** prevista no cronograma:
*   **Entrega:** Notebook `lab_03_eda_basics.ipynb`.
*   **Critério:** O aluno deve demonstrar capacidade de carregar um dataset, identificar corretamente quais colunas são categóricas e quais são numéricas, e aplicar as funções descritivas corretas para cada tipo.

---

## 6. Referências Bibliográficas (Usadas no Planejamento)

*   **Plano de Ensino e Cronograma da Disciplina.**,
*   **McKinney, Wes.** *Python para Análise de Dados*. Novatec. (Capítulos 5, 10 e 12 focados em Pandas, estatística descritiva e dados categóricos).,,