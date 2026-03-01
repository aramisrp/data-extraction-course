# Plano de Aula 07 - Dados Ausentes: Tratamento Univariado (Simples)

**Disciplina:** Extração e Preparação de Dados (IBM8915)
**Professor:** Luís Aramis
**Data:** 05/03 (Quinta-feira)
**Carga Horária:** 2 tempos de 50 minutos (100 min)
**Tópico:** Descarte de dados ausentes e preenchimento (imputação) utilizando estatísticas descritivas básicas.

---

## 1. Objetivos da Aula

### Objetivo Geral

Capacitar os alunos a decidir entre o descarte e o preenchimento de dados ausentes, aplicando técnicas de imputação simples (média, mediana, moda) e avaliando o impacto dessas modificações no conjunto de dados.

### Objetivos Específicos

- **Conceitual:** Compreender os riscos de viés estatístico ao substituir valores ausentes por medidas de tendência central univariadas.
- **Técnico:** Dominar o uso dos métodos `dropna()` e `fillna()` da biblioteca Pandas para tratamento de valores nulos (NA/NaN).
- **Analítico:** Comparar a distribuição dos dados antes e depois da imputação estatística para garantir que a realidade não foi distorcida.

---

## 2. Conteúdo Programático

1.  **Revisão e Estratégias:**
    - Retomada da Aula 06: Quando um "buraco" no dataset é tratável?
    - Deletar vs. Imputar.
2.  **Exclusão de Dados (Listwise/Pairwise Deletion):**
    - O método `dropna()`: exclusão de linhas com qualquer valor ausente vs. exclusão de colunas (`axis=1`).
    - Uso dos parâmetros `how='all'` e limites de tolerância com `thresh`.
3.  **Imputação Univariada com Constantes e Estatísticas:**
    - O método `fillna()` como a "força de trabalho" para substituição de lacunas.
    - Preenchimento com valor constante (ex: `fillna(0)` ou "Desconhecido").
    - Preenchimento estatístico usando `mean()`, `median()` e `mode()`.
    - Preenchimento específico por coluna utilizando dicionários dentro do `fillna()`.

---

## 3. Metodologia e Recursos

- **Metodologia:** Laboratório prático precedido de breve exposição teórica (Demonstração Dialogada). Como analogia, utilizaremos o cenário apresentado na aula anterior: "Passamos de diagnosticadores (Aula 06) para cirurgiões dos dados (Aula 07)".
- **Recursos:** Computador/Projetor, Jupyter Notebook, Pandas.

---

## 4. Cronograma Detalhado (100 min)

### Primeiro Tempo: A Decisão - Descartar ou Preencher (50 min)

| Tempo      | Atividade                                  | Detalhamento do Conteúdo                                                                                                                                                                                        | Fontes de Apoio |
| :--------- | :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------- |
| **10 min** | **Check-in**                               | Conexão com a aula passada. "Visualizamos a gravidade dos nulos. O que fazemos quando 80% da coluna está vazia? E quando apenas 5% está vazia?"                                                                 |                 |
| **20 min** | **Teoria/Prática: A "Faca" (`dropna`)**    | Como e quando descartar. Explicação do método `dropna()`. Demonstração de como descartar apenas linhas onde _todas_ as colunas são nulas (`how='all'`) ou colunas excessivamente vazias.                        |                 |
| **20 min** | **Teoria/Prática: A "Seringa" (`fillna`)** | Introdução ao método `fillna()`. Substituição por constante e o parâmetro `inplace=True` para modificação do objeto original. Passagem de dicionários para preencher diferentes colunas com diferentes valores. |                 |

### Segundo Tempo: Imputação Estatística e Laboratório (50 min)

| Tempo      | Atividade                        | Detalhamento do Conteúdo                                                                                                                                                                                                   | Fontes de Apoio |
| :--------- | :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------- |
| **15 min** | **Imputação com Estatística**    | Como usar estatísticas do próprio dataset para tapar o buraco. Demonstração de `df.fillna(df.mean())`. Discussão sobre distorção da variância e por que variáveis com outliers severos exigem a mediana no lugar da média. |                 |
| **25 min** | **Laboratório Prático (Início)** | Abertura do notebook `lab_05_imputation.ipynb`. Os alunos devem carregar os dados defeituosos do lab anterior, descartar colunas intratáveis (>70% de ausência) e imputar a média/mediana nas tratáveis.                   |                 |
| **10 min** | **Fechamento**                   | Revisão. Explicar a limitação da técnica univariada ("ela não considera correlações com outras colunas") para introduzir a próxima aula: Imputação Multivariada (KNN).                                                     |                 |

---

## 5. Avaliação e Entrega

Como consta no cronograma da disciplina, a avaliação formativa inicia-se com a atividade de **Portfólio (GitHub)** desta semana:

- **Entrega Inicial:** Início do desenvolvimento do notebook `lab_05_imputation.ipynb`.
- **Critério de Avaliação Parcial:** O aluno deverá apresentar o código funcional aplicando corretamente o descarte em colunas altamente esburacadas e preenchendo as colunas restantes com os métodos `fillna(df.mean())` ou `fillna(df.median())` apropriadamente. (O notebook só será finalizado na Aula 08 com métodos multivariados).

---

## 6. Referências Bibliográficas (Para o Professor)

- **Plano de Ensino e Cronograma da Disciplina.**
- **McKinney, Wes.** _Python para Análise de Dados_. (Capítulo 7: Limpeza e preparação dos dados - Seção 7.1: Filtrando dados ausentes e Preenchendo dados ausentes).
