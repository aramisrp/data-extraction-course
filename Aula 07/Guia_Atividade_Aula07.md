# Guia de Atividade Prática - Aula 07: Tratamento de Nulos

**Disciplina:** Extração e Preparação de Dados (IBM8915)  
**Tópico:** Tratar ou amputar? Imputação Univariada Simples no Pandas.

---

## 🎯 Objetivo da Atividade

Sua missão hoje é atuar como o "Cirurgião" dos dados. Iremos colocar em prática duas operações cruciais do Pandas:

1. `dropna()`: Sua faca, para remover partes do dataset que estão podres sem salvação (taxa excessiva de nulos).
2. `fillna()`: Sua seringa para curar colunas afetadas, preservando os dados através da inferência empírica (Média, Mediana e Moda).

Esta atividade compõe o **Portfólio Semanal** avaliativo.

---

## 🛠️ Passo a Passo (O que você precisa fazer)

### No Laboratório (`lab_05_imputation.ipynb`)

Abra o Notebook de Laboratório disponibilizado na aula de hoje. Sua responsabilidade foca nas partes onde aparece a marcação `# ESCREVA SEU CÓDIGO AQUI`.

Você observará a existência de dois pequenos conjuntos de dados gerados em código para facilitar o raciocínio:

- `df_imoveis` (Mão na massa imediata).
- `ecommerce_messy.csv` (No Desafio Cumulativo final da aula).

Para completar a atividade de hoje você tem **três entregáveis no notebook**:

1.  **Amputação (`dropna`):** Você deve configurar os parâmetros adequados no método para derrubar apenas colunas que possuem uma tolerância intolerável de perda (na atividade estipulamos 70% de perda). Use o parâmetro adequado e não se esqueça de usar o `axis=1`.
2.  **Imputação Quantitativa (`fillna` numérico):** Olhe a distribuição da coluna `Preco` dos imóveis (use um simples `.describe()`). Existem outliers ou distribuições severamente desequilibradas? Escolha cirurgicamente entre usar `.mean()` ou `.median()` (atenção para as propriedades numéricas descritas em sala!).
3.  **Imputação Qualitativa (`fillna` categórico):** Como resolver bairros ausentes? Substitua categorias pela moda `.mode()[0]` ou insira adequadamente a constante 'Desconhecido'.

**Importante:** A Parte 3 (_Desafio para Casa_) é altamente encorajada, mas na aula de hoje queremos que sua **Parte 2 do Laboratório** esteja rodando limpa, sem mensagens de erro e, ao rodar `df.isnull().sum()`, todo o retorno seja `0`!

---

## 📈 Critérios de Avaliação (Entrega do Portfólio)

- **Correção da Lógica:** Descartar colunas pelo eixo correto (`axis=1`).
- **Análise Crítica:** Utilizar Mediana (`median`) no lugar da Média em variáveis com outliers explícitos (nossa variável `Preco` dos imóveis).
- **Consistência do Repositório:** O código deve estar hospedado de maneira reprodutível em sua respectiva pasta no Github.

**Aviso de Spoilers:** Essa é a **Etapa 1** da Limpeza. Na Aula 08 veremos técnicas _Multivariadas_ refinadas (Ex: KNN). Codifique simples e eficientemente aqui, pois na aula que vem faremos algoritmos de Inteligência Artificial inferirem as idades faltantes do dataset.

---

## 🚀 Desafio Extra: "Missão Censo Escolar"

Você terminou rápido demais? O professor disponibilizou na mesma pasta o arquivo `censo_escolar_amostra_com_nulos.csv`.

É uma parcela dos dados do censo já conhecida, porém o estagiário acidentalmente apagou milhares de células antes de salvar. Traga suas ferramentas e descubra: **Quantos % da coluna `QT_DOC_BAS` estão faltando e qual técnica você aplicaria nela?**
