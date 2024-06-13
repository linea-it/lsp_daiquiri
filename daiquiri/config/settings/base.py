import os

import daiquiri.core.env as env
import saml2
import saml2.saml

from . import (
    ADDITIONAL_APPS,
    AUTHENTICATION_BACKENDS,
    BASE_DIR,
    BASE_URL,
    DJANGO_APPS,
    LOGIN_URL,
    LOGOUT_URL,
    MIDDLEWARE,
    SETTINGS_EXPORT,
)

SITE_IDENTIFIER = env.get("DOMAIN")
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

LINEA_APPS = [
    "djangosaml2",
]

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

# COmanage Autorization
COMANAGE_SERVER_URL = "https://register.linea.org.br"
COMANAGE_USER = ""
COMANAGE_PASSWORD = ""
COMANAGE_COID = 2

# DJANGO SAML2 Authentication
AUTH_SAML2_ENABLED = env.get_bool("AUTH_SAML2_ENABLED", False)
AUTH_SAML2_LOGIN_URL_CAFE = None
AUTH_SAML2_LOGIN_URL_CILOGON = None

if AUTH_SAML2_ENABLED == True:

    # DOMAIN Exemplo: userquery-dev.linea.org.br
    DOMAIN = env.get("DOMAIN")

    # FQDN Exemplo:https://userquery-dev.linea.org.br
    FQDN = env.get("SITE_URL")
    # FQDN = "https://" + DOMAIN
    CERT_DIR = "certificates"

    # Including SAML2 Backend Authentication
    # AUTHENTICATION_BACKENDS += ("djangosaml2.backends.Saml2Backend", )
    # Custom Saml2 Backend for LIneA
    AUTHENTICATION_BACKENDS += ("linea.saml2.LineaSaml2Backend",)
    # Including SAML2 Middleware
    MIDDLEWARE += ("djangosaml2.middleware.SamlSessionMiddleware",)

    # configurações relativas ao session cookie
    SAML_SESSION_COOKIE_NAME = "saml_session"
    SESSION_COOKIE_SECURE = True

    # Qualquer view que requer um usuário autenticado deve redirecionar o navegador para esta url
    # LOGIN_URL = "/saml2/login/"
    LOGIN_URL = "/login/"
    AUTH_SAML2_LOGIN_URL_CAFE = env.get("AUTH_SAML2_LOGIN_URL_CAFE")
    AUTH_SAML2_LOGIN_URL_CILOGON = env.get("AUTH_SAML2_LOGIN_URL_CILOGON")

    # Encerra a sessão quando o usuário fecha o navegador
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    # Tipo de binding utilizado
    SAML_DEFAULT_BINDING = saml2.BINDING_HTTP_POST
    SAML_IGNORE_LOGOUT_ERRORS = True

    # Serviço de descoberta da cafeexpresso
    # SAML2_DISCO_URL = 'https://ds.cafeexpresso.rnp.br/WAYF.php'

    # Cria usuário Django a partir da asserção SAML caso o mesmo não exista
    SAML_CREATE_UNKNOWN_USER = True

    # https://djangosaml2.readthedocs.io/contents/security.html#content-security-policy
    SAML_CSP_HANDLER = ""

    # URL para redirecionamento após a autenticação
    LOGIN_REDIRECT_URL = "/query"

    SAML_ATTRIBUTE_MAPPING = {
        "eduPersonPrincipalName": ("username",),
        "givenName": ("first_name",),
        "sn": ("last_name",),
        "email": ("email",),
    }

    SAML_CONFIG = {
        # Biblioteca usada para assinatura e criptografia
        "xmlsec_binary": "/usr/bin/xmlsec1",
        "entityid": FQDN + "/saml2/metadata/",
        # Diretório contendo os esquemas de mapeamento de atributo
        "attribute_map_dir": os.path.join(BASE_DIR, "attribute-maps"),
        "description": "SP User Query",
        "service": {
            "sp": {
                "name": "SP User Query",
                "ui_info": {
                    "display_name": {"text": "SP User Query", "lang": "en"},
                    "description": {"text": "SP User Query", "lang": "en"},
                    "information_url": {"text": FQDN, "lang": "en"},
                    "privacy_statement_url": {"text": FQDN, "lang": "en"},
                },
                "name_id_format": [
                    "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent",
                    "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
                ],
                # Indica os endpoints dos serviços fornecidos
                "endpoints": {
                    "assertion_consumer_service": [
                        (FQDN + "/saml2/acs/", saml2.BINDING_HTTP_POST),
                    ],
                    "single_logout_service": [
                        (FQDN + "/saml2/ls/", saml2.BINDING_HTTP_REDIRECT),
                        (FQDN + "/saml2/ls/post", saml2.BINDING_HTTP_POST),
                    ],
                },
                # Algoritmos utilizados
                #'signing_algorithm':  saml2.xmldsig.SIG_RSA_SHA256,
                #'digest_algorithm':  saml2.xmldsig.DIGEST_SHA256,
                "force_authn": False,
                "name_id_format_allow_create": False,
                # Indica que as respostas de autenticação para este SP devem ser assinadas
                "want_response_signed": True,
                # Indica se as solicitações de autenticação enviadas por este SP devem ser assinadas
                "authn_requests_signed": True,
                # Indica se este SP deseja que o IdP envie as asserções assinadas
                "want_assertions_signed": False,
                "only_use_keys_in_metadata": True,
                "allow_unsolicited": False,
            },
        },
        # Indica onde os metadados podem ser encontrados
        "metadata": {
            "local": [
                os.path.join(BASE_DIR, "metadatas", "satosa-prod-cafe.xml"),
                os.path.join(BASE_DIR, "metadatas", "satosa-prod-cilogon.xml"),
            ],
        },
        # Configurado como 1 para fornecer informações de debug
        "debug": 1,
        # Signature
        "key_file": os.path.join(BASE_DIR, CERT_DIR, "mykey.pem"),  # private part
        "cert_file": os.path.join(BASE_DIR, CERT_DIR, "mycert.pem"),  # public part
        # Encriptation
        "encryption_keypairs": [
            {
                "key_file": os.path.join(
                    BASE_DIR, CERT_DIR, "mykey.pem"
                ),  # private part
                "cert_file": os.path.join(
                    BASE_DIR, CERT_DIR, "mycert.pem"
                ),  # public part
            }
        ],
        "contact_person": [
            {
                "given_name": "GIdLab",
                "sur_name": "Equipe",
                "company": "RNP",
                "email_address": "gidlab@rnp.br",
                "contact_type": "technical",
            },
        ],
        # Descreve a organização responsável pelo serviço
        "organization": {
            "name": [("GIdLab", "pt-br")],
            "display_name": [("GIdLab", "pt-br")],
            "url": [("http://gidlab.rnp.br", "pt-br")],
        },
    }

SETTINGS_EXPORT += [
    "AUTH_SAML2_ENABLED",
    "LOGIN_URL",
    "LOGOUT_URL",
]
