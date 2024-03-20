# Daiquiri Application (Django version)

This application is meant to be used with the Django version of the [Daiquiri Framework](https://github.com/aipescience/django-daiquiri).

This project is currently in an early stage of development and by no means production ready.

## Anotações

Manual de Instalação do Daiquiri: <https://django-daiquiri.github.io/docs/installation/>

Autenticação com CILogon:

* <https://django-allauth.readthedocs.io/en/latest/providers.html>
* <https://www.cilogon.org/oidc>

Como escrever querys com ADQL <https://www.cosmos.esa.int/web/gaia-users/archive/writing-queries>

The PHP version of Daiquiri can be found [here](https://github.com/aipescience/daiquiri).

Sobre Cone Search ADQL Postgresql

* <https://gaia.aip.de/cms/services/adql-postgresql/>
* <https://gaia.aip.de/cms/services/cone-search/>

## Development

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

Iniciar o serviço de banco de dados, Na primeira vez é executado o script init_db.sh, que vai criar os dois bancos (admin e catalogs), os schemas e algumas tabelas de exemplo.

```bash
docker-compose up database
```

Procure na saida do terminal por estas mensagens:

```bash
...
lsp_daiquiri-database-1  | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init-db.sh
lsp_daiquiri-database-1  | CREATE DATABASE
lsp_daiquiri-database-1  | CREATE DATABASE
lsp_daiquiri-database-1  | GRANT
lsp_daiquiri-database-1  | CREATE SCHEMA
lsp_daiquiri-database-1  | CREATE SCHEMA
lsp_daiquiri-database-1  | CREATE SCHEMA
...
```

Caso os databases não tenham sido criados na inicialização execute os comandos a seguir para crialos.

```bash
docker-compose exec database psql -U postgres -c "CREATE DATABASE daiquiri_app WITH OWNER postgres;"
docker-compose exec database psql -U postgres -c "CREATE DATABASE daiquiri_data WITH OWNER postgres;"
docker-compose exec database psql -U postgres -c "GRANT CREATE ON DATABASE daiquiri_data TO postgres;"
docker-compose exec database psql -U postgres -d daiquiri_data -c "CREATE SCHEMA tap_schema AUTHORIZATION postgres;CREATE SCHEMA tap_upload AUTHORIZATION postgres;CREATE SCHEMA oai_schema AUTHORIZATION postgres;"
```

Execute estes comandos para importar alguns dados de teste:

```bash
docker-compose exec database psql -U postgres -d daiquiri_data -f /data/gaia_dr2_sample.sql
docker-compose exec database psql -U postgres -d daiquiri_data -f /data/des_dr2_sample.sql
```

```bash
docker-compose up -d
```

```bash
docker-compose exec daiquiri python manage.py createsuperuser
```

[Setup groups](https://django-daiquiri.github.io/docs/administration/)

```bash
docker-compose exec daiquiri python manage.py setup_groups
```

[Setup TAP_SCHEMA](https://django-daiquiri.github.io/docs/administration/)

```bash
docker-compose exec daiquiri python manage.py setup_tap_metadata
```

Load Query Sample Data

```bash
docker-compose exec daiquiri python manage.py loaddata /app/fixtures/query_samples.json
```

Dump Query Sample Data

```bash
docker-compose exec daiquiri python manage.py dumpdata daiquiri_query.example > daiquiri/fixtures/query_samples.json
```

Load Query Sample Data

```bash
docker-compose exec daiquiri python manage.py loaddata /app/fixtures/query_samples.json
```

Build Manual da Imagem docker

```bash
docker build -t linea/lsp_daiquiri:$(git describe --always) .

docker push linea/lsp_daiquiri:5635e8c
```

# TODO: Bug no daiquiri framework quando o tablename tem espaço

# Download VOTable falha se a tabela não tiver os ucds associados as colunas
