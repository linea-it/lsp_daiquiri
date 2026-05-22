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

if [ ! -e /app/static_root/metadata/img/by_gaia.png ]; then
    echo "${NO_COLOR}Copy Gaia License Icon.${NO_COLOR}"
    cp /app/static/daiquiri/imgs/by_gaia.png /app/static_root/metadata/img/by_gaia.png
fi

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

echo "${YELLOW}Running Django with Gunicorn.${NO_COLOR}"
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${DJANGO_GUNICORN_WORKERS:-2} \
    --threads ${DJANGO_GUNICORN_THREADS:-2} \
    --timeout 180 \
    --reload
