Para praticar a limpeza e preparação de dados (Data Wrangling), trabalhar com dados reais e "sujos" é fundamental. O ecossistema de dados públicos brasileiros é uma excelente fonte de desafios, apresentando problemas clássicos como erros de _encoding_, delimitadores confusos, dados ausentes e formatos legados.

Aqui está um guia prático de como encontrar e baixar esses dados em diferentes fontes governamentais e públicas:

### 1. Portal de Dados Abertos (dados.gov.br) e Portal da Transparência

Estes são os repositórios centrais do governo federal e contêm dados de diversas áreas (transportes, saúde, educação).

- **Como baixar:** Acesse o site `dados.gov.br` e pesquise por temas como "Ocorrências Aeronáuticas", "Feminicídio" ou "Solos da Amazônia Legal" e baixe os arquivos diretamente em formato CSV ou XML. Para o Portal da Transparência (dados do Bolsa Família, gastos governamentais), muitas vezes os dados estão em tabelas direto no código HTML, exigindo o uso de técnicas de _Web Scraping_ para extraí-los.
- **Por que são "sujos":**
  - **O Pesadelo do Encoding:** Muitos arquivos governamentais antigos utilizam o padrão de codificação `Latin-1` (ISO-8859-1) em vez do mundial `UTF-8`. Se você abrir sem tratar, palavras como "Amanhã" viram "AmanhÃ£".
  - **Delimitadores e Decimais:** No Brasil, usamos a vírgula para separar casas decimais (ex: R$ 2,50). Por isso, muitos arquivos CSV brasileiros usam o ponto e vírgula (`;`) como separador de colunas em vez da vírgula padrão, o que quebra a leitura tradicional do Pandas.
  - **Integridade:** Datasets como o de acidentes da Polícia Rodoviária Federal possuem uma infinidade de problemas de integridade referencial, dados errados e valores ausentes.

### 2. DATASUS (Ministério da Saúde)

O DATASUS armazena dados críticos sobre o sistema de saúde brasileiro, como o SIM (Sistema de Informações de Mortalidade) e o SIH (Sistema de Informações Hospitalares).

- **Como baixar:** Para ter acesso completo, não use os painéis online limitados. Vá ao menu "Acesso à Informação" > "Serviços" > "Transferência/Download de Arquivos".
- **Por que são "sujos" e complexos:**
  - **Formato Obscuro:** Os arquivos são baixados em um formato compactado antigo chamado `.dbc`, separados por estado, ano e mês. Você precisará baixar um software governamental específico para Windows chamado **TABWIN** para descompactar esses arquivos para o formato `.dbf`, para só então conseguir abri-los no Pandas.
  - **Qualidade do Preenchimento:** Muitas colunas exigem tratamento profundo e olhar crítico. Na base de internações (SIH), por exemplo, a coluna de "raça/cor" é majoritariamente não preenchida (nula) pelos hospitais.

### 3. Consumidor.gov.br (Ministério da Justiça)

Plataforma que registra a interlocução e reclamações diretas entre consumidores e empresas.

- **Como baixar:** O portal de dados do Ministério da Justiça disponibiliza o dicionário de dados e as bases completas separadas por mês, semestre ou ano em formato CSV para download direto.
- **Por que são "sujos":** Por se tratar de reclamações de consumidores, você lidará com dados textuais inseridos por humanos, o que exige limpeza de strings, além da necessidade de concatenar dezenas de arquivos CSV mensais/anuais diferentes para criar uma base histórica única.

### 4. Plataformas de Dados Tratados (Base dos Dados e Brasil.IO)

Mesmo em projetos que já passaram por alguma padronização, a natureza dos dados brasileiros ainda exige limpeza por parte do analista.

- **Base dos Dados:** Oferece acesso via SQL (BigQuery), Python ou R.
  - **Onde está a sujeira:** Em bases como os **Quadros Societários de CNPJ**, a Receita Federal divulga os dados no formato de "fotografias" temporais. Isso significa que, ao baixar dados de datas diferentes, todos os CNPJs se repetem, exigindo tratamento para remover duplicatas. Além disso, bases como a RAIS (Relação Anual de Informações Sociais) possuem códigos institucionais que mudam com o passar dos anos, obrigando o aluno a cruzar os dados com dicionários externos para traduzir a informação.
- **Brasil.IO:** Disponibiliza dados como gastos de deputados, eleições do TSE e casos de Covid-19. Em bases como as do TSE, o próprio portal avisa que nem todos os arquivos estão completos, exigindo tratamento de dados ausentes e parciais.

### 5. Coleta "Selvagem" (Redes Sociais e Literatura)

Se você quer um desafio extremo, pode construir seu próprio dataset extraindo dados de redes sociais e artigos.

- **Por que são "sujos":** Um estudo brasileiro que coletou avistamentos de caravelas-portuguesas em redes sociais relatou a necessidade de aplicar limpeza pesada para corrigir formatos de data diversos, codificação de caracteres quebrada e imprecisões geográficas graves (exigindo o uso de APIs de geocodificação do Google para normalização).
