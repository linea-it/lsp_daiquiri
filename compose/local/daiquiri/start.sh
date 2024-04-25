#!/bin/sh

YELLOW='\033[00;33m'
GREEN="\[\033[0;32m\]"
NO_COLOR='\033[0m'


if [ ! -e /app/vendor ]; then
    echo "${YELLOW}Running Download Vendor.${NO_COLOR}"
    mkdir /app/vendor /app/static
    python manage.py download_vendor_files
fi

python manage.py collectstatic --clear --noinput --verbosity 0

echo "${YELLOW}Running Migrate.${NO_COLOR}"
python manage.py migrate                  # initializes the web database
python manage.py migrate --database tap   # initializes the tap schema in the scientific db
python manage.py migrate --database oai   # initializes the oai schema in the scientific db

echo "${YELLOW}Starting Celery Workers.${NO_COLOR}"
# Antes de iniciar o container remove os arquivos de PID do celery
# O nas settings está configurado para os arquivos ficarem em /tmp
rm -rf /tmp/*.pid
# Executa o comando do daiquiri para iniciar as queues no celery
# O comando le das settings as queues que precisam ser criadas
# e executa o comando celery worker para cada uma delas.
python manage.py workers start

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
    --processes=${DJANGO_UWSGI_PROCESSES:-1} \
    --threads=${DJANGO_UWSGI_THREADS:-1} \
    --http-timeout=180 \
    --py-autoreload=${DJANGO_UWSGI_AUTORELEAD:-1} \
    --static-map /daiquiri_static=/app/static_root
