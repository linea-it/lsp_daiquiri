import os

from . import ADDITIONAL_APPS, BASE_DIR, DJANGO_APPS

SITE_IDENTIFIER = "example.com"
SITE_TITLE = "example.com"
SITE_DESCRIPTION = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."
SITE_LICENSE = "CC0"
SITE_CREATOR = "Anna Admin"
SITE_CONTACT = {
    "name": "Anna Admin",
    "address": "Example Road 1",
    "email": "admin@example.com",
    "telephone": "+01 234 56789",
}
SITE_PUBLISHER = "At vero eos et accusam"
SITE_CREATED = "2019-01-01"
SITE_UPDATED = "2019-04-01"

INSTALLED_APPS = (
    DJANGO_APPS
    + [
        "daiquiri.auth",
        "daiquiri.conesearch",
        "daiquiri.contact",
        "daiquiri.core",
        "daiquiri.datalink",
        "daiquiri.files",
        "daiquiri.jobs",
        "daiquiri.metadata",
        "daiquiri.oai",
        "daiquiri.query",
        "daiquiri.registry",
        "daiquiri.serve",
        "daiquiri.stats",
        "daiquiri.tap",
        "daiquiri.uws",
    ]
    + ADDITIONAL_APPS
)

ACCOUNT_EMAIL_VERIFICATION = "none"

# NÃO ALTERAR: Estas variaveis estão relacionadas a rota /protected/ no ngnix.
# São necessárias para o funcionamento do Download.
# https://django-sendfile2.readthedocs.io/en/latest/backends.html#nginx-backend
SENDFILE_BACKEND = 'django_sendfile.backends.nginx'
SENDFILE_ROOT = '/data/download/'
SENDFILE_URL = '/download'

# NÃO ALTERAR: Esta variavel estão relacionada a rota /daiquiri_static/ no ngnix e no uWSGI.
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/daiquiri_static/"

# Diretorio onde ficam os arquivos de PID do celery
# Não alterar este path por que ele está sendo utilizado no script start.sh
CELERY_PIDFILE_PATH = '/tmp'


SERVE_DOWNLOAD_DIR = '/data/download'