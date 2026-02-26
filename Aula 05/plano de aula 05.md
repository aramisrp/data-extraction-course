# Plano de Aula 05 - Qualidade de Dados e Metadados (Versão Aprofundada)

**Disciplina:** Extração e Preparação de Dados (IBM8915)
**Professor:** Luís Aramis
**Data:** 26/02 (Quinta-feira)
**Carga Horária:** 2 tempos de 50 minutos (100 min)
**Tópico:** Avaliação da saúde dos dados, metadados e construção de dicionários de dados.

---

## 1. Objetivos da Aula

### Objetivo Geral

Avaliar a "saúde" dos dados extraídos, compreendendo que a utilidade dos dados em uma organização deriva de sua correção e confiabilidade. O aluno deve ser capaz de criar um dicionário de dados e identificar inconsistências básicas.

### Objetivos Específicos

- **Conceitual:** Compreender as dimensões da qualidade de dados (acurácia, completude e tempestividade) e classificar metadados em suas quatro categorias principais (negócios, técnico, operacional e de referência).
- **Analítico:** Identificar anomalias, dados codificados incorretamente e artefatos de dados (alterações não intencionais devido a falhas de coleta ou transcrição).
- **Prático (Pandas):** Utilizar funções de auditoria do Pandas (`duplicated()`, `value_counts()`, `isnull()`) para diagnosticar a saúde do dataset.
- **Técnico:** Construir um Dicionário de Dados robusto (`data_dictionary.md`) documentando as definições, as lógicas de negócio e as anomalias encontradas.

---

## 2. Fundamentação Teórica e Conteúdo Programático

### A. Qualidade de Dados (Data Quality)

- **O Paradigma da Sujeira:** "Todos os dados são sujos". O objetivo realista do analista não é alcançar a perfeição utópica, mas tornar os dados _menos sujos_.
- **Garbage-in, Garbage-out:** Se a qualidade da coleta for ruim, a decisão baseada nesses dados também será pobre. É necessário distinguir a _qualidade_ do dado da _utilidade_ do dado.
- **Os 3 Pilares da Qualidade**:
  1.  **Acurácia:** Os dados estão factualmente corretos? Existem duplicatas?.
  2.  **Completude:** Os registros estão completos? Os campos obrigatórios contêm valores válidos?.
  3.  **Tempestividade:** Os registros estão disponíveis em tempo hábil?.

### B. Metadados e o Dicionário de Dados

- Metadados são "dados sobre os dados" e servem como a base para a governança. Eles se dividem em metadados de **Negócios**, **Técnicos**, **Operacionais** e de **Referência**.
- **O Dicionário de Dados:** Atua como um catálogo e repositório centralizado. Será o artefato inicial que documenta o esquema (schema), chaves primárias e lógicas implícitas do projeto.

---

## 3. Ferramentas Analíticas (Aprofundamento em Pandas)

Para aplicar os conceitos de qualidade, os alunos utilizarão o Pandas como ferramenta primária de diagnóstico clínico do dataset:

- **Detecção de Nulos (Completude):** As funções `isnull` e `notnull` no Pandas devem ser utilizadas para detectar dados ausentes. A combinação de `df.isnull().sum()` é a forma mais ágil de quantificar a completude listando a soma de nulos por coluna.
- **Detecção de Duplicatas (Acurácia):** O método `duplicated()` de um DataFrame devolve uma Series booleana informando se cada linha é uma duplicata, ou seja, se foi observada em uma linha anterior. O agrupamento com `sum()` (`df.duplicated().sum()`) revela o volume total do problema.
- **Anomalias Categóricas (Consistência):** O método `.value_counts()` extrai os valores distintos de um array e calcula suas frequências, sendo vital para encontrar categorias raras, erros de digitação (ex: "Masculino" vs "M") e inconsistências de codificação.

---

## 4. Cronograma Detalhado (100 min)

### Primeiro Tempo: Conceitos de Qualidade e Metadados (50 min)

| Tempo      | Atividade                         | Detalhamento do Conteúdo                                                                                                                                       |
| :--------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **10 min** | **Contextualização**              | Introdução ao conceito "Garbage-in, Garbage-out". Discussão: Por que dados perfeitos são uma utopia e qual é o papel do analista para torná-los _menos sujos_? |
| **20 min** | **Teoria: Pilares da Qualidade**  | Apresentação dos 3 pilares: Acurácia, Completude e Tempestividade. Diferenciar utilidade de qualidade.                                                         |
| **20 min** | **Teoria: A Matriz de Metadados** | Explicar que metadados são "dados sobre os dados". Detalhar as 4 classificações e como essas informações compõem a estrutura de um Dicionário de Dados.        |

### Segundo Tempo: Diagnóstico Profundo e Mão na Massa (50 min)

Esta etapa foca na aplicação prática de técnicas de auditoria. Os alunos atuarão como "detetives de dados", investigando anomalias antes de aplicar qualquer técnica destrutiva (como exclusões ou imputações, que ficarão para aulas futuras).

| Tempo      | Atividade                                   | Detalhamento Estratégico e Técnico                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :--------- | :------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **15 min** | **Live Coding:** <br>_Os Sintomas Clínicos_ | **Passo 1: Acurácia (Duplicatas).** Demonstração do uso de `df.duplicated().sum()` para descobrir se há linhas 100% repetidas. Explicar que usar `df[df.duplicated()]` permite visualizar visualmente o que está sendo repetido.<br><br>**Passo 2: Completude (Nulos).** Executar `df.isnull().sum()`. Mostrar como calcular o percentual de nulos dividindo pelo número de linhas (`len(df)`), ajudando a priorizar quais colunas precisam de atenção.<br><br>**Passo 3: Domínio (Categorias).** Usar `df['coluna_categorica'].value_counts()` para auditar entradas textuais. Demonstrar o impacto de variações de caixa (maiúsculas/minúsculas) e sugerir mentalmente o uso futuro de transformações de string (`str.lower()`) ou dicionários de mapeamento (`map()`) para correção. |
| **25 min** | **Laboratório PBL:** <br>_O Dataset Sujo_   | **A Dinâmica:** Entrega de um _dataset_ propositalmente corrompido ou de um contexto real problemático (sem dicionário prévio).<br><br>**A Missão:** Os alunos devem mapear a realidade do dado. Eles devem criar células no Jupyter executando as funções recém-aprendidas para responder: _1. Quantos CPFs/IDs repetidos existem? 2. Qual o grau de preenchimento (nulos) do campo 'Salário'? 3. Existem idades negativas ou categorias como 'Estado=XX'?_<br><br>**O Artefato:** Início simultâneo da redação do arquivo `data_dictionary.md`, confrontando o tipo inferido pelo Pandas (`df.dtypes`) com a expectativa de negócios.                                                                                                                                                 |
| **10 min** | **Fechamento e Práticas Git**               | **Revisão de Markdown:** Demonstração rápida de como criar uma tabela em Markdown para o Dicionário de Dados (Colunas: Variável, Tipo, Descrição, % Nulos, Anomalias Encontradas).<br><br>**Versionamento:** Revisão do fluxo `git add data_dictionary.md`, `git commit -m "Adiciona dicionario e relatorio de qualidade"` e `git push` para entrega da atividade de portfólio.<br><br>**Spoiler:** Preparação conceitual para a Aula 06 e 07, onde aprenderão a tratar os buracos mapeados hoje usando imputações.                                                                                                                                                                                                                                                                     |

---

## 5. Avaliação e Atividade de Portfólio

A avaliação formativa e a entrega principal da Aula 05 compõem a nota do Portfólio (GitHub):

- **Entregável:** Criação do documento `data_dictionary.md` no repositório individual `data-extraction-course`.
- **Critérios de Êxito:**
  1.  **Metadados Técnicos:** Documentação do tipo de dado de cada coluna (schema).
  2.  **Metadados de Negócios:** Descrição clara do que cada coluna representa e sua lógica.
  3.  **Relatório de Qualidade:** Inclusão obrigatória de uma seção no dicionário (ou notas nas colunas) apontando todas as anomalias descobertas durante a exploração com o Pandas, focando no nível de completude (nulos) e na identificação de duplicatas estruturais ou ruídos categóricos.
