# LIneA User Query (Development)

This application is meant to be used with the Django version of the [Daiquiri Framework](https://github.com/aipescience/django-daiquiri).

>This project is currently in an early stage of development and by no means production ready.

## Requirements

- Docker version 25.0.1
- git version 2.39.3
- Vscode + devcontainer extension
- Acesso ao banco de dados desdb4 - **prod_gavo**


## Development URLs

- **Github Repository:** <https://github.com/linea-it/lsp_daiquiri>
- **Docker Repository:** <https://hub.docker.com/repository/docker/linea/lsp_daiquiri/general>
- **Daiquiri:** <http://localhost/>
- **Django Admin:** <http://localhost/admin/>
- **Celery Flower:** <http://localhost/flower/>
- **Rabbitmq:** <http://localhost/rabbitmq/>


## Docs

- **Daiquiri Docs:** <https://django-daiquiri.github.io/docs>
- **Daiquiri Instalation**: <https://django-daiquiri.github.io/docs/installation/>
- **Daiquiri Framework:** <https://github.com/django-daiquiri/daiquiri>
- **Daiquiri App:** <https://github.com/django-daiquiri/app>
- **GAIA@AIP:** <https://gaia.aip.de/>
- **MUSE-Wide:** <https://musewide.aip.de/>
- **GAIA How to API access**: <https://gaia.aip.de/cms/services/scripted-access/>

## Setup Development Environment

Este projeto possui **devcontainer** configurado, mas é necessário executar a instalação convencional primeiro. depois de feito estes passos, basta abrir o vscode na pasta do projeto e executar o devcontainer normalmente.


>Este passos foram escritos considerando :
>
>- Maquina local do desenvolvedor
>- Usuario 1000 Grupo 1000
>- Instalação feita no path: `/home/<user>/linea/tno`

---

Clone Repository, create directories and copy local settings.

```bash
git clone https://github.com/linea-it/lsp_daiquiri.git daiquiri \
&& cd daiquiri \
&& mkdir -p data data/download data/files data/upload logs \
&& chmod -R g+w data logs \
&& cp compose/local/local_settings_sample.py local_settings.py \
&& cp compose/local/.env.sample .env \
&& cp compose/local/nginx-proxy.conf nginx-proxy.conf \
&& cp compose/local/docker-compose.yml docker-compose.yml 

```

Build Docker images

```bash
docker compose build
```

Inicie o serviço de banco de dados. Na primeira vez será executado o script `init_db.sh`, que vai criar os dois bancos (daiquiri_admin e daiquiri_data), os schemas e algumas tabelas de exemplo.

```bash
docker compose up database
```

Procure na saida do terminal por esta mensagem: `LOG:  database system is ready to accept connections`
Após a inicialização do banco de dados, pare o serviço com comando `CTRL+C`. 

Agora inicie o serviço daiquiri.
```bash
docker compose up daiquiri
```
Espere pelas mensagens: 
```bash
daiquiri-1  | *** uWSGI is running in multiple interpreter mode ***
daiquiri-1  | spawned uWSGI master process ...
```
Após o daiquiri ter sido iniciado corretamente, encerre o serviço com comando `CTRL+C`. 

### Start all services in background
O parametro `-d` coloca todos os serviços para executar em background não prendendo o terminal. 

```bash
docker compose up -d
```

A saida do comando informa se todos os serviços foram iniciados corretamente. 

```bash
[+] Running 5/5
 ✔ Container daiquiri-database-1       Started            0.0s  
 ✔ Container daiquiri-rabbit-1         Started            0.0s
 ✔ Container daiquiri-daiquiri-1       Started            0.0s
 ✔ Container daiquiri-celery_flower-1  Started            0.0s
 ✔ Container daiquiri-nginx-1          Started            0.0s
```


### Configuração Inicial do Daiquiri

Os Comandos a seguir são executados **com todos os serviços ligados**.

Crie um usuario administrativo no Django.
```bash
docker compose exec daiquiri python manage.py createsuperuser
```
Estes comandos são expecificos do Daiquiri:
[Setup groups](https://django-daiquiri.github.io/docs/administration/)

```bash
docker compose exec daiquiri python manage.py setup_groups
```

[Setup TAP_SCHEMA](https://django-daiquiri.github.io/docs/administration/)

```bash
docker compose exec daiquiri python manage.py setup_tap_metadata
```

Load Query Sample Data

```bash
docker compose exec daiquiri python manage.py loaddata /app/fixtures/query_samples.json
```

Neste ponto o ambiente está pronto. Acesse a url localhost no navegador e teste o ambiente.

## Useful commands

### Stop all services

```bash
docker compose stop
```

### Services stats

```bash
docker compose stats
```

### Open bash in backend container

with backend service running

```bash
docker-compose exec backend bash
```

### Dump Query Sample Data

```bash
docker-compose exec daiquiri python manage.py dumpdata daiquiri_query.example > daiquiri/fixtures/query_samples.json
```

### Build Manual da Imagem docker
Estando logado no dockerhub pelo terminal execute o build e o push da imagem do daiquiri.

Docker Hub: <https://hub.docker.com/repository/docker/linea/lsp_daiquiri/>

A identificação unica de cada imagem pode ser o numero de versão exemplo: `linea/lsp_daiquiri:v0.1` ou o hash do commit para versões de desenvolvimento: `linea/lsp_daiquiri:8816330`. 

>Para obter o hash do commit usar o comando `$(git describe --always)`

```bash
docker build -t linea/lsp_daiquiri:$(git describe --always) .

docker push linea/lsp_daiquiri:$(git describe --always)
```

## Anotações

Manual de Instalação do Daiquiri: <https://django-daiquiri.github.io/docs/installation/>

Como escrever querys com ADQL <https://www.cosmos.esa.int/web/gaia-users/archive/writing-queries>

Sobre Cone Search ADQL Postgresql

* <https://gaia.aip.de/cms/services/adql-postgresql/>
* <https://gaia.aip.de/cms/services/cone-search/>

Autenticação com CILogon (Para estudo/testes):

* <https://django-allauth.readthedocs.io/en/latest/providers.html>
* <https://www.cilogon.org/oidc>



### TODOS: 

- Bug no daiquiri framework quando o tablename tem espaço (foi aberto issue no repositório oficial)
- Download VOTable falha se a tabela não tiver os ucds associados as colunas (foi aberto issue no repositório oficial)
