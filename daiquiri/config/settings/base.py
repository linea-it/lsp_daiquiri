import os

import daiquiri.core.env as env

from . import (
    ADDITIONAL_APPS,
    AUTHENTICATION_BACKENDS,
    BASE_URL,
    DJANGO_APPS,
    LOGIN_URL,
    LOGOUT_URL,
    MIDDLEWARE,
    SETTINGS_EXPORT,
)

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

LINEA_APPS = ["shibboleth"]

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
    + LINEA_APPS
)

ACCOUNT_EMAIL_VERIFICATION = "none"

# NÃO ALTERAR: Estas variaveis estão relacionadas a rota /protected/ no ngnix.
# São necessárias para o funcionamento do Download.
# https://django-sendfile2.readthedocs.io/en/latest/backends.html#nginx-backend
SENDFILE_BACKEND = "django_sendfile.backends.nginx"
SENDFILE_ROOT = "/data/download/"
SENDFILE_URL = "/download"

# NÃO ALTERAR: Esta variavel estão relacionada a rota /daiquiri_static/ no ngnix e no uWSGI.
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/daiquiri_static/"

# Diretorio onde ficam os arquivos de PID do celery
# Não alterar este path por que ele está sendo utilizado no script start.sh
CELERY_PIDFILE_PATH = "/tmp"


SERVE_DOWNLOAD_DIR = "/data/download"

ANNOUNCEMENT_MESSAGE_FILTER = "linea.filters.LineaMessageFilter"

CONESEARCH_ADAPTER = "daiquiri.conesearch.adapter.SimpleConeSearchAdapter"
CONESEARCH_ANONYMOUS = True
CONESEARCH_SCHEMA = "des_dr2"
CONESEARCH_TABLE = "coadd_objects"
CONESEARCH_SUBJECTS = ["cone search"]

QUERY_FORMS = [
    {
        "key": "sql",
        "label": "SQL query",
        "service": "query/js/forms/sql.js",
        "template": "query/query_form_sql.html",
    },
    # {
    #     "key": "cone",
    #     "label": "Cone search",
    #     "service": "query/js/forms/cone.js",
    #     "template": "query/query_form_cone.html",
    # },
    {
        "key": "upload",
        "label": "Upload VOTable",
        "service": "query/js/forms/upload.js",
        "template": "query/query_form_upload.html",
    },
]


# -----------------------------------------------
# LInea Specific
# -----------------------------------------------

# Em desenvolvimento não é possivel acessar o Shibboleth
# Desenvolvedores devem usar a auth nativa do Django.

# Shibboleth Authentication
AUTH_SHIB_ENABLED = env.get_bool("AUTH_SHIB_ENABLED")

if AUTH_SHIB_ENABLED == True:
    LINEA_LOGIN_URL = env.get_url("AUTH_SHIB_LOGIN_URL").strip("/")

    # SHIB_LOGIN_GOOGLE_URL = env.get_url('AUTH_SHIB_LOGIN_URL_GOOGLE_URL').strip('/')

    # TODO: Não sei se logout tem uma url diferente. temporariamente recebe o valor que já tinha.
    LINEA_LOGOUT_URL = LOGOUT_URL

    # Essas variaveis são usadas internamente no django no fluxo de autenticação.
    LOGIN_URL = LINEA_LOGIN_URL.strip("/")
    LOGOUT_URL = LINEA_LOGOUT_URL

    # Including Shibboleth Middleware
    MIDDLEWARE.append(
        "linea.shibboleth.ShibbolethMiddleware",
    )

    # Usar essa url depois de logado para ver os atributos disponiveis
    # https://userquery-dev.linea.org.br/Shibboleth.sso/Session

    # https://github.com/Brown-University-Library/django-shibboleth-remoteuser
    SHIBBOLETH_ATTRIBUTE_MAP = {
        "eppn": (True, "username"),
        "cn": (True, "first_name"),
        "sn": (True, "last_name"),
        "Shib-inetOrgPerson-mail": (False, "email"),
        # "mail": (True, "email"),
    }

    # Including Shibboleth authentication:
    AUTHENTICATION_BACKENDS += ("shibboleth.backends.ShibbolethRemoteUserBackend",)

SETTINGS_EXPORT += [
    "AUTH_SHIB_ENABLED",
    "LOGIN_URL",
    "LOGOUT_URL"
]
