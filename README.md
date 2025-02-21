# DESAFIO TÉCNICO

## Objetivo
O projeto consiste em duas etapas. A primeira é criar um fluxo de dados para extrair e carregar os dados de GPS do BRT gerados em uma API usando a ferramenta Prefect. 
Esses dados devem ser extraídos a cada minuto, e em seguida, transformados em arquivo csv. Depois, esses dados em csv
devem ser carregados em um banco PostgreSQL.
Na segunda etapa é criar um modelo no dbt que gere uma tabela derivada a partir da tabela armazenada no banco Postgres, contendo o id, a posição e a velocidade do BRT.

Link da API: https://dados.mobilidade.rio/gps/brt

## Estrutura do projeto
- dbt_project: diretório dbt contendo o modelo que gera a tabela derivada 'brt_gps_transformed_data.sql' e o arquivo 'source.yml' com os dados do banco Postgresql que o modelo usa como fonte de dados
- brt_data_flow.py: workflow in Python que faz a extração, transformação em csv e carregamento dos dados no Postgres usando o Prefect
- docker-compose.yml: arquivo Docker compose que permite construir uma instância do banco PostgreSQL dentro de um container docker
- brt_data.csv: arquivo csv que é gerado ao executar o script 'brt_data_flow.py' 
- profiles.yml: arquivo de configuração que contém credenciais de conexão com o banco que o dbt usa
- requirements.txt: arquivo que contém as bibliotecas necessárias para o projeto


## Pré-requisitos
- Ter o Python 3.9 ou 3.10 instalado, pois algumas bibliotecas não funcionam com versões superiores ou inferiores. No meu ambiente, usei o Python 3.10.14. Recomendo usar o mesmo.

Para instalar o python no Linux (Debian/Ubuntu) usando o repositório:

```
sudo apt-get install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt-get install python3.10

# para instalar bibliotecas que podem estar ausentes e ajudam na criação de ambiente virtual
sudo apt install python3.10-venv python3.10-dev python3.10-distutils
```

- Ter o Docker Engine e o Docker compose instalado (Usei a versão para WSL2 no Windows):

https://docs.docker.com/desktop/setup/install/windows-install/

https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository (usando o repositório apt no Ubuntu)



## Execução
Obs: todos os comandos listados a seguir foram executados em um terminal do sistema Linux Ubuntu. Caso seu sistema seja diferente, verificar os comandos correspondentes no mesmo.

- clonar o repositório do projeto:

    `git clone git@github.com:Priscaruso/desafio_sms.git`
- criar um ambiente virtual para instalação dos pacotes necessários

    `python3.10 -m venv venv`
- ativar ambiente virtual criado

    `source venv/bin/activate`

- atualizar o pip, caso necessário

    `pip install --upgrade pip`

- instalar os pacotes necessários contidos no arquivo requirements.txt

    `pip install -r requirements.txt`
- construir o container com o Postgres usando o Docker compose file

    `sudo docker compose up -d`
- verificar se o container foi criado corretamente

    `docker ps`
- rodar o script python que executa o workflow em segundo plano

    `python3.10 brt_data_flow.py &`
- acessar o banco pelo container docker para verificar tabela 'gps_brt'criada
    ```
    docker exec -it postgres_db psql -U docker -d brt_data
    \dt  # lista as tabelas do banco
    select * from gps_brt;
    q    # para sair da exibição dos dados
    \q   # para sair do banco
    ```

- criar a pasta .dbt no seu diretório ~

    `mkdir -p ~/.dbt`

- mover o arquivo profiles.yml para dentro da pasta ~/.dbt

    `mv profiles.yml ~/.dbt`
- executar o modelo dbt 'brt_gps_transformed_data.sql' para gerar a tabela derivada
    ```
    cd dbt_project
    dbt run --select brt_gps_transformed_data.sql
    ```
- acessar o banco novamente pelo container docker para verificar a tabela derivada
    ```
    docker exec -it postgres_db psql -U docker -d brt_data
    \dt # lista as tabelas do banco
    select * from brt_gps_transformed_data
    q   # para sair da exibição dos dados
    \q  # para sair do banco
    ```
- fechar o terminal para encerrar o workflow em segundo plano