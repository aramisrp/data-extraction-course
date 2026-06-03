# Guia Prático: Configurando Conexões no Apache Airflow

Este tutorial é um guia passo a passo para configurar as conexões de banco de dados (**SQLite** e **PostgreSQL**) na interface gráfica do Apache Airflow. As *Connections* são fundamentais para que suas DAGs consigam se comunicar com sistemas externos de forma segura.

---

## 1. Entendendo as Connections
No Airflow, você **nunca** deve colocar senhas, logins ou portas diretamente no código Python da sua DAG (hardcoding). Em vez disso, você cadastra as credenciais no cofre do Airflow e no código você chama apenas o ID dessa conexão (ex: `postgres_default` ou `sqlite_default`).

O Airflow usa "Providers" para saber como se comunicar com cada tipo de sistema.

---

## 2. Configurando o SQLite (Banco Local e Leve)

O SQLite é excelente para testes e aprendizado porque ele salva todo o banco de dados em um único arquivo local (`.db`), não exigindo a instalação de um servidor de banco de dados robusto.

### Pré-requisito
O provedor do SQLite normalmente já vem instalado por padrão no Airflow.
Se não estiver, o comando de instalação é: `pip install apache-airflow-providers-sqlite`

### Passo a Passo (Interface Web)
1. Abra a interface web do Airflow (geralmente em `http://localhost:8080`).
2. No menu superior, clique em **Admin** e depois em **Connections**.
3. Clique no botão azul com o ícone de **+ (Add a new record)**.
4. Preencha o formulário exatamente da seguinte maneira:
   - **Connection Id:** `sqlite_default` *(Este é o nome que você usará no código)*
   - **Connection Type:** `SQLite`
   - **Host:** `/tmp/meu_banco_airflow.db` *(Caminho absoluto de onde o arquivo do banco será salvo. No Windows, você pode usar algo como `C:/Users/Usuario/meu_banco.db`)*
5. Os demais campos (Login, Password, Port) devem ficar **em branco**, pois o SQLite não utiliza autenticação de rede.
6. Clique em **Save**.

### Testando no Código
```python
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

tarefa_sqlite = SQLExecuteQueryOperator(
    task_id='teste_sqlite',
    conn_id='sqlite_default', # O mesmo ID cadastrado na interface!
    sql="SELECT 1;"
)
```

---

## 3. Configurando o PostgreSQL (Banco Relacional de Mercado)

O PostgreSQL é o banco de dados relacional open-source mais utilizado na Engenharia de Dados. Ele roda como um serviço (frequentemente dentro de um container Docker).

### Pré-requisito
Você precisa ter o *provider* do Postgres instalado no seu ambiente Airflow.
Comando: `pip install apache-airflow-providers-postgres`

Além disso, você precisa de um servidor PostgreSQL rodando e acessível. 

### Passo a Passo (Interface Web)
1. Na interface web do Airflow, vá em **Admin $\rightarrow$ Connections**.
2. Clique no botão azul **+ (Add a new record)**.
3. Preencha o formulário com os dados do seu servidor Postgres:
   - **Connection Id:** `postgres_default`
   - **Connection Type:** `Postgres`
   - **Host:** `localhost` *(Ou `host.docker.internal` se o Airflow estiver no Docker e o Postgres no seu Windows, ou o IP do servidor na nuvem)*
   - **Database / Schema:** `postgres` *(Ou o nome do banco de dados que você criou)*
   - **Login:** `postgres` *(Seu usuário do banco)*
   - **Password:** `sua_senha_secreta`
   - **Port:** `5432` *(Porta padrão do Postgres)*
4. Clique no botão **Test** (se disponível na sua versão do Airflow) para garantir que a conexão foi bem sucedida.
5. Clique em **Save**.

### Testando no Código
```python
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

tarefa_postgres = SQLExecuteQueryOperator(
    task_id='teste_postgres',
    conn_id='postgres_default', # O mesmo ID cadastrado na interface!
    sql="SELECT 1;"
)
```

---

## 💡 Dicas de Solução de Problemas (Troubleshooting)

- **A opção "SQLite" ou "Postgres" não aparece no menu "Connection Type":** Isso significa que o pacote do provider não está instalado no seu ambiente Python onde o Airflow roda. Pare o Airflow, rode o `pip install` adequado e reinicie o Airflow.
- **Erro "Connection Refused" no Postgres:** Verifique se o seu servidor Postgres está realmente ligado, se a porta (5432) está correta e se o `Host` está certo. Se você usa Docker no Windows (WSL2), o host `localhost` pode não funcionar de dentro de um container do Airflow apontando para a máquina física; use `host.docker.internal`.
- **Erro "OperationalError: unable to open database file" no SQLite:** O Airflow não tem permissão de escrita na pasta que você especificou no campo `Host`, ou o caminho não existe. Tente criar o caminho em uma pasta de usuário (ex: `/tmp/` no Linux/Mac ou `C:/Temp/` no Windows).
