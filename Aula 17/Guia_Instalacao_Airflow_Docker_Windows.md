# Guia de Instalação: Apache Airflow com Docker Desktop (Windows)

Este tutorial ensina como criar um ambiente de Engenharia de Dados instalando o Apache Airflow em sua máquina Windows utilizando o **Docker Desktop** nativamente, sem a necessidade de acessar o terminal do Linux (WSL).

---

## 1. Pré-requisitos

1. **Docker Desktop:** Você deve ter o [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/) instalado e rodando em sua máquina.
2. Certifique-se de que o ícone do Docker (a baleia) está verde na barra de tarefas do Windows.

---

## 2. Preparando a Estrutura de Diretórios (Prompt de Comando)

Abra o seu **Prompt de Comando (CMD)** ou **PowerShell** no Windows e crie uma pasta onde os arquivos do seu projeto Airflow irão morar. 

```cmd
REM 1. Crie uma pasta para o projeto e entre nela
mkdir C:\Users\%USERNAME%\meu_projeto_airflow
cd C:\Users\%USERNAME%\meu_projeto_airflow

REM 2. Crie as subpastas essenciais do Airflow
mkdir dags
mkdir logs
mkdir plugins
mkdir config

REM 3. Crie o arquivo .env para definir o usuario (No Windows, o ID padrao usado pelo Airflow e 50000)
REM O comando 'cmd /c' garante que o PowerShell nao estrague a codificacao do arquivo (UTF-16)
cmd /c "echo AIRFLOW_UID=50000 > .env"
```

---

## 3. Baixando o Docker Compose Oficial do Airflow

A equipe do Apache Airflow mantém um arquivo de orquestração oficial para subir todos os contêineres necessários (Scheduler, Webserver, PostgreSQL, Redis).

No mesmo PowerShell, utilize o utilitário nativo `curl.exe` do Windows para baixar o arquivo YAML:

```cmd
curl.exe -LfO "https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml"
```

*Verifique se o arquivo `docker-compose.yaml` apareceu na pasta.*

---

## 4. Inicializando o Banco de Dados do Airflow

O Airflow guarda todas as informações em um banco de dados próprio (o Postgres que vem no Compose). Antes de iniciar o Airflow, precisamos criar as tabelas desse banco.

Ainda no CMD/PowerShell, execute:
```cmd
docker-compose up airflow-init
```

Aguarde o download das imagens (pode demorar na primeira vez). Ao final, você deve ver uma mensagem dizendo `airflow-init_1 exited with code 0`. (Código 0 significa que a inicialização ocorreu com sucesso).

---

## 5. Subindo o Ambiente (O Grande Momento!)

Agora que o banco está inicializado, basta ligar todos os serviços:

```cmd
REM O parametro '-d' libera o terminal para voce continuar usando
docker-compose up -d
```

### O que o Docker ligou na sua máquina?
Você pode abrir o aplicativo do Docker Desktop para ver os contêineres rodando:
- **`airflow-webserver`**: A interface visual no navegador.
- **`airflow-scheduler`**: O cérebro que dispara as DAGs.
- **`postgres`**: O banco de dados do Airflow.
- **`redis` & `airflow-worker`**: O sistema de filas onde as tarefas executam.

---

## 6. Acessando a Interface

Abra o seu navegador (Chrome, Edge, etc) e digite:
**`http://localhost:8080`**

- **Usuário padrão:** `airflow`
- **Senha padrão:** `airflow`

### Onde eu coloco meus códigos Python?
Para colocar o **seu** código:
1. Abra o explorador de arquivos do Windows e vá até a pasta `C:\Users\SeuUsuario\meu_projeto_airflow\dags`.
2. Salve seu script Python (ex: `meu_pipeline.py`) dentro desta pasta.
3. Volte para o navegador (`localhost:8080`) e o arquivo aparecerá na interface do Airflow automaticamente (aperte F5 após alguns segundos).

---

## 7. Como Desligar Tudo

Para economizar a memória e bateria do seu computador, desligue os contêineres quando terminar de estudar. 

No CMD/PowerShell, na mesma pasta do projeto, digite:
```cmd
docker-compose down
```
*(Nota: Isso desliga e remove os contêineres temporários, mas não deleta seus arquivos Python nem os dados do banco. Quando você rodar `docker-compose up -d` novamente, tudo continuará lá).*
