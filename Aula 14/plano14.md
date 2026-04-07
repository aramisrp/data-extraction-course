### Plano de Aula 14 - Engenharia de Software para Dados: Transformadores Customizados e Divisão de Dados
**Disciplina:** Extração e Preparação de Dados (IBM8915)
**Data:** 07/04 (Terça-feira)
**Carga Horária:** 2 tempos de 50 minutos (100 min)
**Tópico:** Nivelamento sobre a divisão Treino/Teste (80/20), Orientação a Objetos Básica em Python e a criação de classes customizadas para integração em pipelines.

---

#### 1. Objetivos da Aula

##### Objetivo Geral
Nivelar o conhecimento analítico da turma sobre a necessidade fundamental do isolamento de dados (Treino vs. Teste) para evitar o *overfitting* e, em seguida, capacitá-los a escrever código testável com classes Python, criando transformadores de dados próprios que respeitem as regras arquiteturais do *Scikit-Learn*.

##### Objetivos Específicos
*   **Analítico (Nivelamento):** Compreender a separação de 80% dos dados para treino e 20% para teste, assimilando a importância da generalização (não "decorar o gabarito").
*   **Técnico (POO):** Aprender os fundamentos de Programação Orientada a Objetos em Python, dominando conceitos como `class`, o método construtor `__init__` e a palavra-chave `self` para criar lógicas de negócio exclusivas.
*   **Técnico (Scikit-Learn):** Aprender a herdar as classes base `BaseEstimator` e `TransformerMixin` para construir objetos compatíveis com *Pipelines* contínuos.
*   **Arquitetural:** Desenvolver a mentalidade de modularização, extraindo o código solto do Jupyter Notebook para um script puro e reutilizável (`custom_transformers.py`).

---

#### 2. Conteúdo Programático

1.  **Nivelamento Analítico e Fundamentos:**
    *   A analogia do Aluno e a Prova: Nivelamento sobre a divisão 80/20 e a função `train_test_split`.
    *   O Artesão vs. O Engenheiro: O limite das "peças prontas" de Lego do Scikit-Learn e a necessidade de fabricarmos nossas próprias máquinas de transformação.
2.  **Orientação a Objetos Básica em Python:**
    *   O que é uma `class` e como o método construtor `__init__` funciona na memória do computador.
    *   A palavra-chave `self` e como o objeto guarda informações do treinamento internamente para uso futuro.
3.  **A Anatomia de um Transformador do Scikit-Learn:**
    *   A herança múltipla de classes: `class MeuTransformador(BaseEstimator, TransformerMixin):`.
    *   A aplicação do Nivelamento no Código: O método `.fit()` é a fase de **estudo** (enxerga só os 80%). O método `.transform()` é a **prova** (aplicado aos 20% sem vazar dados).
4.  **Modularização de Código (Engenharia de Software):**
    *   Exportar o código de dentro do Jupyter para um script puro em Python (`custom_transformers.py`) e importá-lo de volta no fluxo de trabalho.

---

#### 3. Metodologia e Recursos
*   **Metodologia:** A aula inicia com o **Nivelamento Teórico** focado em *Storytelling* analítico para garantir que todos os alunos compreendam a base estatística (80/20) e o objetivo da arquitetura de software. Em seguida, transição para *Live Coding* profundo (Programação em Pares), saindo do ambiente procedural direto para a Orientação a Objetos. O uso de "Worked Examples" (apresentar a solução completa para o aluno estudar) guiará o laboratório prático.
*   **Recursos:** Jupyter Notebook, Editor de Texto/IDE (como VS Code) para escrever o arquivo `.py`, bibliotecas Pandas e Scikit-Learn.

---

#### 4. Cronograma Detalhado (100 min)

##### Primeiro Tempo: Nivelamento Analítico e Orientação a Objetos (50 min)
| Tempo | Atividade | Detalhamento do Conteúdo |
| :--- | :--- | :--- |
| **15 min** | **Nivelamento: A Prova e o Lego** | **Estabelecimento da Linha de Base:** Se o professor dá as 100 questões da prova antes, o aluno tira 10 porque decorou o gabarito (*Overfitting*). Explicar que a máquina precisa de 80% para "estudar" e 20% trancados num cofre para "testar" a generalização. Conectar isso com a necessidade de fabricar nossas próprias "peças de Lego" (Classes) quando o Scikit-Learn não possui a regra de negócio que precisamos. |
| **15 min** | **Teoria e Prática: POO em Python** | Breve aula de Orientação a Objetos. Criar uma classe vazia. Mostrar como o método construtor `__init__` e o parâmetro `self` funcionam para armazenar as variáveis e o estado internamente na memória do computador. |
| **20 min** | **O Contrato do Scikit-Learn** | *Live coding*: Construir o esqueleto herdando `BaseEstimator` e `TransformerMixin`. Fazer a conexão matadora com o nivelamento inicial: "O método `.fit()` é onde a nossa peça de Lego senta e estuda a base de 80%. O método `.transform()` é como ela faz a prova na base de 20% usando estritamente o que aprendeu." |

##### Segundo Tempo: Laboratório de Construção e Exportação (50 min)
| Tempo | Atividade | Detalhamento do Conteúdo |
| :--- | :--- | :--- |
| **15 min** | **Desenvolvendo a Lógica** | Preencher a classe criada. **Exemplo prático:** Criar um transformador chamado `ConversorTemporal` que pega colunas de data brutas, transforma para `datetime` e cria a flag `Is_Weekend` (lógica construída nas aulas anteriores) garantindo que tudo funcione perfeitamente dentro dos métodos da classe Orientada a Objetos. |
| **20 min** | **Laboratório (Exportação)** | Início do laboratório prático. Os alunos deverão extrair o código dessa classe complexa de dentro do Jupyter Notebook e salvá-lo em um arquivo em branco chamado **`custom_transformers.py`** usando o VS Code ou editor de texto padrão. |
| **15 min** | **Teste e Importação** | Voltar ao Jupyter Notebook. Rodar `from custom_transformers import ConversorTemporal`. Dividir a base real usando `train_test_split` (80/20), colocar o objeto recém-criado dentro de um `Pipeline` e testar se ele executa o fluxo inteiro sem vazar dados do futuro para o passado. |

---

#### 5. Avaliação e Entrega de Portfólio (GitHub)
*   **Entregáveis:** O aluno deverá subir o **arquivo `custom_transformers.py`** e o Notebook atualizado no seu repositório oficial da disciplina no GitHub.
*   **Critérios de Êxito:**
    1. O arquivo `.py` deve conter a classe funcional escrita em Python puro.
    2. A classe deve herdar corretamente as propriedades do Scikit-Learn e respeitar a assinatura dos argumentos `X` e `y`.
    3. A execução final no Notebook deve separar perfeitamente a lógica de aprendizado (`.fit()`) da lógica de aplicação (`.transform()`), provando que o nivelamento analítico foi absorvido e não há recalculo de regras de negócio na base de Teste (20%).