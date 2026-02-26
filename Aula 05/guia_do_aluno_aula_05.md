# Guia do Aluno - Aula 05: Qualidade de Dados e Metadados

## 🎯 Objetivo da Atividade

Nesta atividade de laboratório (PBL), você atuará como um **"detetive de dados"**. Seu objetivo é diagnosticar a "saúde" de um conjunto de dados corrompido, compreendendo sua realidade e construindo o seu dicionário de dados (apontando as anomalias encontradas) antes de aplicar qualquer técnica de limpeza ou alteração definitiva.

Lembre-se: _Garbage-in, Garbage-out!_ Nossa missão hoje não é atingir a perfeição utópica, mas entender quão sujos os dados estão.

---

## 🛠️ Ferramentas Necessárias

- **Linguagem / Biblioteca:** Python e Pandas
- **Ambiente:** Jupyter Notebook, Google Colab ou equivalente
- **Versionamento:** Git & GitHub (para integração no portfólio)

---

## 📝 Passo a Passo da Missão

### Passo 1: O Diagnóstico Clínico (Mão na Massa no Pandas)

Carregue o dataset problemático fornecido na aula em um Jupyter Notebook. A partir daí, utilize as bibliotecas aprendidas para investigar o dado. Crie células em seu notebook para responder às seguintes perguntas de pesquisa sobre a saúde do dado:

1. **Acurácia (Detecção de Duplicatas):**
   - _Existem duplicatas no dataset? Quantos registros inteiros ou IDs repetidos existem?_
   - 💡 **Dicas:**
     - Utilize `df.duplicated().sum()` para contar o volume do problema.
     - Para visualizar as linhas ofensoras, inspecione-as com `df[df.duplicated()]`.

2. **Completude (Detecção de Nulos/Ausentes):**
   - _Qual é o grau de preenchimento dos campos? Qual o volume de nulos no campo 'Salário' (ou nas variáveis críticas do seu dataset)?_
   - 💡 **Dicas:**
     - Obtenha o somatório total de ausentes com `df.isnull().sum()`.
     - Calcule o **percentual de nulos** para priorizar seu esforço dividindo pelos totais de linhas: `df.isnull().sum() / len(df)`.

3. **Consistência e Metadados (Anomalias Categóricas e de Domínio):**
   - _Os dados de negócio fazem sentido? Existem idades negativas, erros de digitação (ex: "Masculino" vs "M") ou categorias estranhas como 'Estado=XX'?_
   - 💡 **Dicas:**
     - Levante os valores distintos e suas frequências em variáveis textuais/categóricas utilizando a função `df['coluna_categorica'].value_counts()`.

---

### Passo 2: Construção do Dicionário de Dados

Enquanto realiza as auditorias da etapa anterior (confrontando o `df.dtypes` do Pandas com o que deveria ser a realidade do dado), você deve documentar todas as suas descobertas.

Crie um arquivo chamado **`data_dictionary.md`** (em Markdown). Este arquivo vai atuar como o catálogo centralizado de metadados deste dataset. O dicionário **deve** conter uma tabela formatada com as colunas abaixo:

- **Variável:** Nome da coluna no dataset.
- **Tipo:** A tipagem técnica esperada para a coluna (Inteiro, Decimal, Texto, Data, Booleano, etc).
- **Descrição:** O metadado de negócios. O que aquele campo representa no mundo real e qual a lógica por trás dele.
- **% Nulos:** O percentual de completude identificado pelo Pandas.
- **Anomalias Encontradas:** O _relatório de qualidade_, detalhando se há duplicações, ruídos categóricos ou valores impossíveis.

_Exemplo de formatação da tabela Markdown:_

```markdown
| Variável     | Tipo    | Descrição                                              | % Nulos | Anomalias Encontradas                                                                     |
| :----------- | :------ | :----------------------------------------------------- | :------ | :---------------------------------------------------------------------------------------- |
| `ID_Cliente` | Inteiro | Identificador único referencial de clientes do varejo. | 0%      | 5 IDs repetidos.                                                                          |
| `Idade`      | Inteiro | Idade do cliente em anos (Tempo de vida).              | 3.5%    | Existem valores inconsistentes como idades negativas (-5, -10).                           |
| `Estado`     | Texto   | Sigla da Unidade Federativa da federação (UF).         | 0%      | Discrepâncias de tipografia (contém "sp" minúsculo) e anomalias sistêmicas (contém "XX"). |
```

---

### Passo 3: Fechamento e Entrega de Portfólio

A conclusão desta atividade de mapeamento e documentação da saúde da base de dados integra a avaliação do seu Portfólio individual.

1. Finalize o seu arquivo `data_dictionary.md`.
2. Salve no seu repositório local e versione essa etapa executando, no terminal, a sequência de comandos Git:

```bash
git add data_dictionary.md
git commit -m "Adiciona dicionario e relatorio de qualidade - Aula 05"
git push origin main
```

---

## 🚀 Spoiler: E os próximos passos?

Guarde muito bem este relatório! Agora vocês já possuem a visibilidade completa da "doença" dos dados. Nas próximas sessões (Aulas 06 e 07), o diagnóstico dará lugar ao "tratamento". Vocês utilizarão técnicas construtivas (e destrutivas) através do Pandas para realizar imputações e correções. Bom trabalho, detetives! 🔍📊
