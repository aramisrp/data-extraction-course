# Plano de Aula 03 - Extração de Dados: Bancos de Dados Relacionais (SQL)

**Disciplina:** Extração e Preparação de Dados (IBM8915)  
**Professor:** Luís Aramis  
**Data:** 19/02 (Quinta-feira)  
**Carga Horária:** 2 aulas de 50 minutos (100 min)  
**Tópico:** Conexão e extração de dados de Bancos SQL

## 1. Objetivos da Aula

### Objetivo Geral
Capacitar os alunos a conectar aplicações Python a bancos de dados relacionais e executar consultas SQL para extração de datasets.

### Objetivos Específicos
*   Compreender a estrutura básica de um banco de dados relacional (Tabelas, Colunas, Chaves).
*   Escrever consultas SQL básicas (SELECT, WHERE, JOIN, GROUP BY) focadas em leitura de dados.
*   Utilizar a biblioteca `pandas` e `SQLAlchemy`/`sqlite3` para conectar e extrair dados diretamente para um DataFrame.
*   Comparar a extração via SQL com a leitura de arquivos planos (CSV/Excel).

## 2. Conteúdo Programático
1.  **Revisão rápida:** Arquivos planos vs Bancos de Dados.
2.  **Fundamentos de SQL:**
    *   Comando `SELECT` e cláusula `FROM`.
    *   Filtragem com `WHERE`.
    *   Ordenação e Limitação (`ORDER BY`, `LIMIT`).
    *   Noções de JOIN (Juntar tabelas).
3.  **Python + SQL:**
    *   Conceito de Connection String.
    *   Uso de `pd.read_sql_query` e `pd.read_sql_table`.
    *   Persistência: Salvar resultado da query em arquivo local (CSV/Parquet).

## 3. Metodologia
*   **Aula Expositiva Dialogada (20%):** Introdução aos conceitos teóricos com exemplos no quadro/slide.
*   **Laboratório Prático (80%):** Resolução de desafios de extração utilizando um banco de dados SQLite de exemplo (e.g., Chinook ou Northwind) dentro do Jupyter Notebook.

## 4. Recursos Didáticos
*   Computador do professor com projetor multimídia.
*   Laboratório de informática ou notebooks pessoais dos alunos.
*   Ambiente configurado com Python 3.9+, Pandas e SQLAlchemy.
*   Arquivo de banco de dados SQLite de exemplo (`chinook.db` ou similar).

## 5. Cronograma (2 aulas de 50 min)

### Aula 1: Introdução ao SQL e Consultas Básicas (50 min)

| Tempo | Atividade | Descrição |
| :--- | :--- | :--- |
| **10 min** | **Boas-vindas e Contextualização** | Revisão da aula anterior (arquivos planos). Discussão: Por que as empresas usam Bancos de Dados Relacionais e não apenas Excel? |
| **15 min** | **Teoria: SQL Básico** | Explicação da sintaxe básica SQL: `SELECT`, `FROM`, `WHERE`. Diferença entre DDL (CREATE) e DML (SELECT). Foco em *Leitura*. |
| **20 min** | **Prática Guiada (SQL)** | Alunos abrem uma ferramenta de conexão (DBeaver ou extensão do VS Code/Notebook) e executam suas primeiras queries no banco de exemplo. |
| **05 min** | **Fechamento Aula 1** | Dúvidas rápidas e intervalo. |

### Aula 2: Conexão Python e Extração de Datasets (50 min)

| Tempo | Atividade | Descrição |
| :--- | :--- | :--- |
| **10 min** | **Teoria: Conexão Python-SQL** | Como o Python "fala" com o Banco? Introdução a drivers e ORMs (SQLAlchemy). O método mágico `pd.read_sql`. |
| **30 min** | **Laboratório Prático** | Resolução do notebook `lab_02_sql_extraction.ipynb`. Desafio: Extrair uma tabela filtrada, fazer um JOIN simples e exportar o resultado para CSV. |
| **05 min** | **Discussão de Metadados** | Como saber o esquema do banco? Importância da documentação e de explorar o `information_schema` (ou equivalente). |
| **05 min** | **Encerramento** | Revisão dos objetivos alcançados. Chamada para a próxima aula (Análise Exploratória). |

## 6. Avaliação
A avaliação será formativa, baseada na participação durante a aula e na conclusão dos exercícios propostos no notebook `lab_02_sql_extraction.ipynb`.

## 7. Bibliografia
*   **Básica:** CASTRO, L.N. Introdução à Mineração de Dados (Capítulo sobre Pré-processamento).
*   **Básica:** McKINNEY, Wes. *Python para Análise de Dados: Tratamento de Dados com Pandas, NumPy e IPython*. Novatec / O'Reilly. (Capítulo sobre Carregamento de Dados, Armazenamento e Formatos de Arquivo - Seção: Interagindo com Web APIs e Bancos de Dados).
*   **Complementar:** NIELD, Thomas. *Introdução à Linguagem SQL: Abordagem Prática para Iniciantes*. O'Reilly / Novatec.
*   **Documentação:** [Pandas IO Tools - SQL Queries](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#sql-queries)
