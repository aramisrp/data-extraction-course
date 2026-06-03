# Guia de Instalação: Apache Airflow Nativo no WSL2 (Sem Docker)

Este tutorial ensina a realizar a instalação "oficial" e nativa do Apache Airflow em um ambiente Windows através do **WSL2** (Windows Subsystem for Linux), utilizando Python puro, **sem depender do Docker**. 

O Airflow foi desenhado para rodar nativamente em ambientes Linux. O WSL2 nos dá exatamente isso dentro do Windows.

---

## 1. Pré-requisitos

1. **WSL2 Instalado:** Você deve ter uma distribuição Linux rodando no Windows. Se não tiver, abra o PowerShell como Administrador, rode o comando `wsl --install` e reinicie o computador.
2. **Distribuição Padrão:** Geralmente, o Ubuntu é a distribuição padrão. Abra o menu Iniciar, digite "Ubuntu" e abra o terminal Linux.

---

## 2. Preparando o Ambiente Python (Terminal do WSL)

Abra o seu terminal do **Ubuntu** (WSL). O Ubuntu já vem com o Python, mas precisamos garantir que o gerenciador de pacotes (`pip`) e o ambiente virtual (`venv`) estejam prontos.

Rode os comandos abaixo (se pedir senha, é a senha que você criou ao abrir o Ubuntu pela primeira vez):

```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

Agora, vamos criar uma pasta para o nosso projeto e um ambiente virtual isolado:

```bash
# 1. Cria a pasta e entra nela
mkdir ~/meu_airflow
cd ~/meu_airflow

# 2. Cria o ambiente virtual chamado "venv"
python3 -m venv venv

# 3. Ativa o ambiente virtual (Voce vera (venv) no comeco da linha)
source venv/bin/activate
```

---

## 3. Instalando o Apache Airflow Oficial

A instalação oficial recomenda o uso de "constraints" para garantir que as versões das dependências não quebrem o Airflow. 

Com o ambiente virtual ativado, defina onde o Airflow deve salvar seus arquivos (o `AIRFLOW_HOME`):

```bash
# Define a pasta atual como a "casa" do Airflow
export AIRFLOW_HOME=~/meu_airflow

# Define a versao do Airflow e do Python para instalar a versao correta
AIRFLOW_VERSION=3.2.1
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

# URL da Constraint oficial da fundacao Apache
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Executa a instalacao via PIP
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```
*Dica: A instalação pode demorar alguns minutos. Tenha paciência!*

---

## 4. Inicializando o Banco de Dados Local (SQLite)

Diferente da versão Docker que sobe um Postgres gigante, a instalação nativa do Airflow usa por padrão um banco leve (**SQLite**) armazenado localmente para salvar os históricos das execuções.

Para inicializar o banco de dados interno e criar o seu usuário administrador, execute:

```bash
# 1. Cria as tabelas no SQLite
airflow db migrate

# 2. Cria o seu usuario de acesso (Troque a senha se preferir)
airflow users create \
    --username admin \
    --firstname Professor \
    --lastname IBMEC \
    --role Admin \
    --email admin@ibmec.com \
    --password admin
```

---

## 5. Ligando os Motores (Webserver e Scheduler)

O Airflow precisa de dois processos rodando ao mesmo tempo:
1. O **Webserver** (A interface gráfica que você abre no navegador).
2. O **Scheduler** (O cérebro que dispara as DAGs nos horários certos).

Como eles precisam rodar ao mesmo tempo, você precisará de **duas abas de terminal** do Ubuntu abertas.

### No Terminal 1 (Ligando a Interface):
```bash
# Lembre de ativar o ambiente virtual primeiro
cd ~/meu_airflow
source venv/bin/activate
export AIRFLOW_HOME=~/meu_airflow

# Liga o Webserver na porta 8080
airflow webserver --port 8080
```

### No Terminal 2 (Ligando o Cérebro):
Abra uma nova janela do Ubuntu (WSL).
```bash
# Ativa o ambiente novamente nesta nova tela
cd ~/meu_airflow
source venv/bin/activate
export AIRFLOW_HOME=~/meu_airflow

# Liga o Agendador
airflow scheduler
```

---

## 6. Acessando a Interface e Criando DAGs

Com os dois terminais rodando:
1. Abra o navegador no Windows (Chrome/Edge).
2. Acesse: **`http://localhost:8080`**
3. Faça login com o usuário e senha que criamos no Passo 4 (`admin` e `admin`).

### Onde coloco meus códigos?
Dentro da pasta `~/meu_airflow`, o Airflow lerá automaticamente os scripts Python se você criar uma subpasta chamada `dags`.

```bash
# (Em um terceiro terminal)
cd ~/meu_airflow
mkdir dags
```
Qualquer script salvo em `~/meu_airflow/dags` aparecerá na interface web!

---

## 7. Como Desligar Tudo

Para desligar o Airflow, vá em cada um dos dois terminais abertos (o do Webserver e o do Scheduler) e pressione as teclas **`CTRL + C`**. Isso encerrará os processos com segurança.
