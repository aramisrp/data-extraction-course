# Guia de Instalação: Apache Airflow com Docker e WSL2

Este tutorial ensina como criar um ambiente profissional de Engenharia de Dados instalando o Apache Airflow em sua máquina Windows utilizando a arquitetura do **WSL2** (Windows Subsystem for Linux) integrada ao **Docker Desktop**.

Essa é a recomendação oficial da fundação Apache para desenvolvimento local no Windows.

---

## 1. Pré-requisitos

Antes de iniciar, certifique-se de que sua máquina atende aos requisitos abaixo:
1. **WSL2 Instalado:** Você deve ter uma distribuição Linux rodando no Windows. Se não tiver, abra o PowerShell como Administrador e rode o comando `wsl --install`. Reinicie o computador.
2. **Docker Desktop:** Baixe o [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/) e instale-o.
3. **Integração do Docker com WSL2:** 
   - Abra o Docker Desktop.
   - Vá nas Configurações (ícone de engrenagem no topo direito) $\rightarrow$ **Resources** $\rightarrow$ **WSL Integration**.
   - Marque a caixa *“Enable integration with my default WSL distro”* e ative o botão correspondente à sua distribuição (ex: Ubuntu).

---

## 2. Preparando a Estrutura de Diretórios

Abra o seu terminal do **Ubuntu** (ou a distribuição WSL instalada) e crie uma pasta onde os arquivos do seu projeto Airflow irão morar. Nunca rode isso em pastas sensíveis do sistema; crie um diretório de projetos isolado.

```bash
# 1. Crie uma pasta para o projeto e entre nela
mkdir meu_projeto_airflow
cd meu_projeto_airflow

# 2. Crie as subpastas que o Airflow precisa mapear para o seu Linux
mkdir dags logs plugins config

# 3. Defina a variável de ambiente do usuário do Airflow (Evita erros de permissão)
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
*(Nota: O passo 3 diz ao Docker que o Airflow vai rodar com o mesmo ID do seu usuário do Linux local, o que impede problemas onde o Docker cria arquivos e você não consegue deletá-los depois).*

---

## 3. Baixando o Docker Compose Oficial do Airflow

A equipe do Apache Airflow mantém um arquivo de orquestração oficial para subir todos os contêineres necessários de uma vez (Scheduler, Webserver, PostgreSQL, Redis e CeleryWorkers).

No mesmo terminal do Ubuntu (dentro da pasta `meu_projeto_airflow`), rode o comando para baixar o arquivo YAML:

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

---

## 4. Inicializando o Banco de Dados do Airflow

O Airflow guarda todas as informações (quais DAGs existem, log de erros, usuários) em um banco de dados próprio (o Postgres que vem embutido no Compose). Antes de iniciar o Airflow pela primeira vez, precisamos criar as tabelas desse banco.

Execute o comando:
```bash
docker-compose up airflow-init
```

Aguarde o download das imagens e a execução. Ao final, você deve ver uma mensagem verde dizendo `airflow-init_1 exited with code 0`. (Código 0 significa sucesso absoluto; qualquer outro código significa que houve erro).

---

## 5. Subindo o Ambiente (O Grande Momento!)

Agora que o banco está inicializado, basta ligar todos os serviços do Airflow:

```bash
# O '-d' significa 'detached', ou seja, o terminal ficara liberado apos o comando
docker-compose up -d
```

### O que acabou de subir?
O Docker ligou uma frota de sistemas trabalhando juntos na sua máquina:
- **`airflow-webserver`**: A interface visual que você vai acessar no navegador.
- **`airflow-scheduler`**: O "cérebro" que olha as DAGs e decide quando executá-las.
- **`postgres`**: O banco de dados do próprio Airflow.
- **`redis` & `airflow-worker`**: O sistema de filas (Celery) onde as tarefas pesadas de fato executam.

---

## 6. Acessando a Interface

Abra o navegador no seu Windows (Chrome, Edge, etc) e digite:
**`http://localhost:8080`**

- **Usuário padrão:** `airflow`
- **Senha padrão:** `airflow`

### Onde eu coloco meus códigos Python?
Você vai notar que na interface há várias DAGs de "Exemplo". Para colocar o **seu** código:
1. Volte ao seu WSL.
2. Abra a pasta `dags` que você criou no Passo 2 (Pode usar o VSCode digitando `code dags/` no terminal).
3. Salve seu arquivo Python (ex: `meu_pipeline.py`) dentro desta pasta.
4. O arquivo aparecerá magicamente na interface do Airflow (pode demorar alguns segundos, aperte F5).

---

## 7. Como Desligar Tudo

Sua bateria vai sofrer se você deixar esses contêineres rodando eternamente quando não estiver estudando. Para desligar tudo de forma segura, abra o terminal do WSL na pasta do projeto e digite:

```bash
docker-compose down
```
*(Nota: O `down` desliga e deleta os contêineres, mas **NÃO** deleta suas DAGs nem o banco de dados. Quando você der `docker-compose up -d` novamente amanhã, tudo estará lá).*
