#!/bin/sh

YELLOW='\033[00;33m'
GREEN="\[\033[0;32m\]"
NO_COLOR='\033[0m'

# Se nao tiver o manage.py e a primeira vez que o container e executado, apenas abre o terminal.
if [ -e manage.py ]
then
    python manage.py migrate                  # initializes the web database
    python manage.py migrate --database tap   # initializes the tap schema in the scientific db
    python manage.py migrate --database oai   # initializes the oai schema in the scientific db

    echo "${YELLOW}Running Download Vendor Files.${NO_COLOR}"
    python manage.py download_vendor_files    # dowloads front-end files from the CDN
    # python manage.py collectstatic --clear --noinput --verbosity 0

    # python manage.py runworker default &> $LOG_DIR/celery.log  &
    # python manage.py runworker query
    # python manage.py runworker download &> $LOG_DIR/celery.log  &

    # python manage.py runserver

    # Para produção é necessário usar o uWSGI!
    # uWSGI para servir o app e ter compatibilidade com Shibboleth
    # https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html
    # TODO: Em produção não é recomendado o auto reload. utilizar uma variavel de ambiente para ligar ou desligar esta opção.
    echo "${YELLOW}Running Django with uWSGI.${NO_COLOR}"
    uwsgi \
        --socket 0.0.0.0:8000 \
        --wsgi-file /app/config/wsgi.py \
        --module config.wsgi:application \
        --buffer-size=32768 \
        --processes=4 \
        --threads=2 \
        --http-timeout=120 \
        --py-autoreload=1 \
        --static-map /daiquiri_static=/app/static_root
else
    /bin/bash
fi