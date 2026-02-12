# Aula 02: Extração de Dados
## Arquivos Planos (CSV e Excel)

*   **Disciplina:** Extração e Preparação de Dados (IBM8915)
*   **Professor:** Luís Aramis
*   **Data:** 12/02

<!--
Bom dia, pessoal! Bem-vindos à nossa segunda aula. Hoje vamos sair da teoria e começar a colocar a mão na massa. O objetivo do dia é aprender a trazer dados do 'mundo selvagem' para dentro do nosso ambiente Python. Vamos focar nos formatos mais comuns que vocês encontrarão no mercado: arquivos planos, como CSVs e planilhas Excel.
-->

---

# Agenda do Dia

1.  **Check-in:** Recapitulando Aula 01 (10 min)
2.  **Estudo de Caso:** O Desastre do Excel (UK Covid) (20 min)
3.  **Conceitos:** Arquivos Planos, Encoding e Delimitadores (20 min)
4.  **Live Coding:** Pandas `read_csv` e `read_excel` na prática (20 min)
5.  **Laboratório:** Desafio prático no VS Code (40 min)
6.  **Encerramento:** Spoiler da próxima aula e Atividade para Casa.

<!--
Esta é a nossa agenda. Começaremos reaquecendo os motores, passaremos para os conceitos fundamentais – entender o que é um CSV e por que encoding dá tanto trabalho – e depois eu vou codar ao vivo com vocês. A segunda metade da aula é toda de vocês, resolvendo problemas reais no Jupyter Notebook.
-->

---

# Estudo de Caso: "O Desastre do Excel"
## UK Covid-19 (2020)

*   **O Problema:** O governo britânico "perdeu" 15.841 casos positivos de Covid.
*   **A Causa:** Uso de arquivo Excel antigo (`.xls`) para processar os dados.
*   **O Limite:** O formato `.xls` suporta apenas 65.536 linhas.
*   **O Resultado:** Dados excedentes foram cortados silenciosamente.

> **Lição:** Planilhas não são bancos de dados. Para Big Data, precisamos de Python/Pandas.

<!--
Antes de abrir o código, quero contar uma história de terror. Em 2020, no auge da pandemia, o Reino Unido perdeu o rastro de 16 mil pessoas infectadas. O motivo? Alguém usou um Excel antigo (.xls) que só aceitava 65 mil linhas. O arquivo encheu, e o Excel cortou o resto silenciosamente. Isso mostra por que NÃO podemos confiar cegamente em planilhas para volume de dados. É aqui que entra o Python.
-->

---

# A Realidade Brasileira
## O Portal da Transparência (dados.gov.br)

Dois problemas clássicos:

1.  **Separador Decimal:**
    *   Brasil: Vírgula (R$ 2,50) -> CSV usa **Ponto e Vírgula (;)**.
    *   EUA: Ponto ($ 2.50) -> CSV usa Vírgula (,).
2.  **Encoding:**
    *   Mundo: **UTF-8**.
    *   Brasil (Legado/Governo): **Latin-1** (ISO-8859-1).
    *   Sintoma: `Amanhã` vira `AmanhÃ£`.

<!--
Trazendo para a nossa realidade: se vocês baixarem dados do governo agora, vão ter problemas. Primeiro: o CSV deles não é separado por vírgula, mas por ponto e vírgula, porque a nossa vírgula já é usada nos centavos. Segundo: o encoding. Eles usam padrões antigos (Latin-1) que quebram toda a acentuação se você abrir como UTF-8. Hoje vamos aprender a domar esses dois monstros.
-->

---

# Por que Extração de Dados?

> "Garbage In, Garbage Out"

*   A qualidade da análise depende da qualidade da ingestão.
*   Extração é **Auditoria**:
    *   Dados completos?
    *   Tipos corretos (Número vs Texto)?
    *   Encoding preservado?

<!--
Lembram do que falamos sobre 'Garbage In, Garbage Out'? Se a gente importar os dados errado agora, nosso modelo de IA lá na frente vai falhar. Extração é checagem. É garantir que o número '1.000' não virou o texto '1.000' ou que o acento do 'João' não virou um símbolo estranho.
-->

---

# O Universo dos Arquivos Planos

## CSV (Comma Separated Values)
*   **Texto Puro:** Leve e Universal.
*   **Pegadinha:** O separador pode variar (`;`, `|`, `\t`).

## Excel (.xlsx)
*   **Binário:** Estruturado e Pesado.
*   **Recursos:** Múltiplas abas, fórmulas, formatação.

<!--
No mercado, vocês vão lidar principalmente com esses dois caras. O CSV é o rei da interoperabilidade: é texto puro, leve, qualquer sistema gera. Mas a pegadinha é o nome: 'Comma Separated'. No Brasil, usamos vírgula para decimais (R$ 2,50), então nossos CSVs geralmente usam PONTO E VÍRGULA como separador. Já o Excel é mais rico, tem abas, mas é mais pesado e 'fechado'.
-->

---

# O Pesadelo do Encoding

**O que é?** Tradução de bits (`010101`) para caracteres (`ç`, `ã`).

### Padrões Comuns:
*   **UTF-8:** Padrão Mundial (Use sempre que possível).
*   **Latin-1 (ISO-8859-1):** Legado Brasil (Bancos, Governo).
*   **CP1252:** Windows Antigo.

**Erro Comum:** `UnicodeDecodeError` ou caracteres quebrados.

<!--
Quem aqui já abriu um arquivo e viu caracteres estranhos onde deveria ter acentos? Isso é erro de encoding. É como tentar ler um livro em alemão usando um dicionário de inglês. O pandas assume UTF-8 por padrão. Se o arquivo foi salvo no Excel antigo (Latin-1), vai dar erro. Vamos aprender a corrigir isso.
-->

---

# Pandas ao Resgate (Live Coding)

```python
import pandas as pd

# O jeito fácil
df = pd.read_csv('arquivo.csv')

# O modo "Brasil" (Realidade)
df = pd.read_csv('arquivo.csv', 
                 sep=';',           # Separador
                 encoding='latin1', # Codificação
                 decimal=',')       # Decimal

# Excel
df_excel = pd.read_excel('planilha.xlsx', sheet_name='Aba2')
```

<!--
Agora vou abrir o VS Code e mostrar na prática. Prestem atenção nesses parâmetros: `sep`, `encoding` e `decimal`. Eles são o 'kit de primeiros socorros' do Cientista de Dados brasileiro. Se o arquivo não abre de primeira, provavelmente a solução está em um desses três.
-->

---

# Inspeção Inicial (Sanity Check)

**Sempre execute após carregar:**

1.  `df.head()`: Cabeçalhos e primeiras linhas estão ok?
2.  `df.info()`: Tipos de dados (Dtypes) e Nulos.
3.  `df.shape`: Contagem de Linhas x Colunas bate?
4.  `df.describe()`: Resumo estatístico rápido (Média, Max, Min).

<!--
Carregou o arquivo? Não saia fazendo gráficos! Faça o 'Sanity Check'. O `head` mostra se o cabeçalho foi lido certo. O `info` mostra se a coluna de preço é número ou virou texto (object). O `shape` diz se você perdeu linhas no caminho. Isso é procedimento padrão, tem que estar no sangue.
-->

---

# Atividade Prática (Lab 01)

### Hands-on no VS Code
1.  **Clone/Atualize** o repositório do curso.
2.  Abra a pasta `Aula 02`.
3.  Abra o notebook `lab_01_flat_files.ipynb`.

**Desafio:** Carregar 4 arquivos com problemas reais (delimitadores, encoding, metadados).

**Tempo:** 40 minutos.

<!--
Agora é com vocês. Preparei um notebook com quatro desafios. Um arquivo separado por pipe, um Excel com cabeçalho deslocado, um CSV do IBGE com metadados 'sujando' o início... Usem o que acabamos de ver. Estou passando nas mesas para ajudar.
-->

---

# Parte 2 (Avançado)

*   **Chunksize:** Ler arquivos gigantes em pedaços.
*   **On Bad Lines:** Ignorar linhas quebradas (`error`, `skip`, `warn`).
*   **Glob:** Ler múltiplos arquivos de uma pasta em lote.

<!--
Para quem terminou rápido: o notebook tem uma seção 'Avançado'. Dêm uma olhada no `chunksize`. É assim que a gente lê arquivos de 5GB num computador com 4GB de RAM.
-->

---

# Atividade Para Casa (Portfólio)
### Parte 2: Dados Reais

1.  Acesse **dados.gov.br** ou **Kaggle**.
2.  Baixe um CSV de tema livre.
3.  Carregue no Pandas (tratando erros).
4.  Gere `.info()` e `.describe()`.
5.  **Commit no GitHub** até a próxima aula.

<!--
O dever de casa é simples: quero ver vocês lidando com a vida real. Escolham um dataset que gostem – futebol, economia, saúde – baixem e carreguem. Quero ver o código no GitHub de vocês antes da próxima aula.
-->

---

# Próxima Aula: SQL

*   Saindo de arquivos estáticos.
*   Conectando em **Bancos de Dados Relacionais**.
*   Consultas `SELECT` direto para o Pandas.

**Dica:** Instalem a extensão "SQLite Viewer" no VS Code.

<!--
Na quinta-feira, vamos subir o nível. Vamos parar de trocar arquivos e vamos conectar direto na fonte: Bancos de Dados SQL. Obrigado a todos!
-->
