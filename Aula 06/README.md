# Guia de Atividade Prática - Aula 06: Mapeamento de Nulos

**Disciplina:** Extração e Preparação de Dados (IBM8915)  
**Tópico:** O primeiro passo da faxina: Identificação Visual e Quantitativa.

---

## 🎯 Objetivo da Atividade

Nesta aula, antes de pensarmos em _como_ tratar um problema, precisamos ser capazes de medí-lo e visualizá-lo com clareza. Você atuará como o detetive do dataset, quantificando buracos nas bases e construindo uma visualização clara (Gráfico de Barras) que alerte o nível de risco de cada coluna.

Esta atividade inicia o seu **Portfólio Semanal** (primeira parte).

---

## 🛠️ Passo a Passo (O que você precisa fazer)

### No Laboratório (`lab_04_missing_values_viz.ipynb`)

Abra o Notebook da Atividade. Nós providenciamos um dataset sujo real de dados clínicos de pacientes (`dados_clinicos_brutos.csv`).

A sua missão é preencher as lacunas de código descritas abaixo:

1.  **Carregamento e Inspeção Básica:**
    - Leia o CSV corretamente (cuidado com separadores e decimais).
    - Use `df.info()` e um breve olhar no cabeçalho.

2.  **O Sensor de Nulos (Quantificação):**
    - Utilize `.isnull().sum()` para descobrir quantas informações clínicas "vazaram" para cada variável.
    - **O mais importante:** Crie uma variável (`percentual_nulos`) que calcule e guarde a proporção matemática (de 0 a 100%) da ausência de dados de forma automática, independemente do tamanho do `.csv` que o estagiário subir no sistema amanhã. (Dica na Cheat Sheet!)

3.  **Visualização Gráfica do Problema:**
    - Baseado no seu cálculo de proporção, plote um gráfico de barras usando Matplotlib, Pandas Plot ou Seaborn com o ranking das colunas mais deficitárias (e.g., O eixo X traz o nome da coluna, o Y a % de nulos).
    - Você extrairá _insights_. Baseado nas regras de corte mencionadas em sala de aula (Ex: "Colunas com > 70% de nulos dificilmente têm salvação"), quais atributos você estaria inclinado a jogar fora na próxima aula e quais você tentaria salvar?

---

## 📈 Critérios de Avaliação (Entrega do Portfólio)

- **Precisão Geométrica:** O cálculo da porcentagem estar perfeitamente formatado.
- **Clareza Visual:** O gráfico deve possuir título, rótulos (labels) legíveis nos eixos X e Y. Gráficos "em branco" ou que cortam o nome da coluna no eixo inferior perdem pontuação.
- **Repositório:** O material (Notebook) commitado corretamente no GitHub do aluno.

---

## 🚑 Desafio de Interpretação: MCAR, MAR ou MNAR?

Olhe profundamente para as colunas faltantes do dataset de saúde. Se notarmos que a coluna **"Pressão Arterial"** falha predominantemente em perfis onde a **"Idade"** é inferior a 18 anos, que tipo de mecanismo de ausência nós enfrentamos? (Responda mentalmente e venha debater com a turma!).
