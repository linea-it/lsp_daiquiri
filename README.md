Daiquiri Application (Django version)
=====================================

Instalation: <https://django-daiquiri.github.io/docs/installation/>

Autenticação com CILogon:

- <https://django-allauth.readthedocs.io/en/latest/providers.html>
- <https://www.cilogon.org/oidc>

Como escrever querys com ADQL <https://www.cosmos.esa.int/web/gaia-users/archive/writing-queries>

This application is meant to be used with the Django version of the [Daiquiri Framework](https://github.com/aipescience/django-daiquiri).

This project is currently in an early stage of development and by no means production ready.

The PHP version of Daiquiri can be found [here](https://github.com/aipescience/daiquiri).

Copy Enviroment file and config 
```bash
cp .env.sample .env
cp local_sample.py local.py
```

Create Dirs

```bash
mkdir data data/files data/download data/upload data/log data/log/celery data/log/daiquiri
```

```bash
docker-compose run daiquiri python manage.py sqlcreate
```

OU

```bash
docker-compose exec database psql -U postgres -c "CREATE DATABASE daiquiri_app WITH OWNER postgres;"
docker-compose exec database psql -U postgres -c "CREATE DATABASE daiquiri_data WITH OWNER postgres;"
docker-compose exec database psql -U postgres -c "GRANT CREATE ON DATABASE daiquiri_data TO postgres;"
docker-compose exec database psql -U postgres -d daiquiri_data -c "CREATE SCHEMA tap_schema AUTHORIZATION postgres;CREATE SCHEMA tap_upload AUTHORIZATION postgres;CREATE SCHEMA oai_schema AUTHORIZATION postgres;"
```

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


# TODO: Bug no daiquiri framework quando o tablename tem espaço!
# Download VOTable falha se a tabela não tiver os ucds associados as colunas
