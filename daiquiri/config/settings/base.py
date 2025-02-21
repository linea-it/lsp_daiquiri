import os

import saml2
import saml2.saml
from django.utils.translation import gettext_lazy as _

import daiquiri.core.env as env

from . import (
    ADDITIONAL_APPS,
    AUTHENTICATION_BACKENDS,
    BASE_DIR,
    BASE_URL,
    DJANGO_APPS,
    LICENSE_CHOICES,
    LICENSE_IDENTIFIERS,
    LICENSE_URLS,
    LOGIN_URL,
    LOGOUT_URL,
    MIDDLEWARE,
    SETTINGS_EXPORT,
)

# the hostname and port number of the current Server
BASE_HOST = env.get("SITE_URL")

# Public URL of the Daiquiri site. Used for VO and OAI metadata.
# Default: http://localhost:8000
SITE_URL = env.get("SITE_URL")

# Identifier for the Daiquiri site. Usually the URL without the protocol. Used for VO and OAI metadata.
# Default: None
SITE_IDENTIFIER = env.get("DOMAIN")
# The title for the Daiquiri site. Used for VO and OAI metadata.
# Default: None
SITE_TITLE = "LIneA TAP Service"

# The description for the Daiquiri site. Used for VO and OAI metadata.
# Default: None
SITE_DESCRIPTION = "The TAP Service registry for linea.org.br"

# A license for the Daiquiri site.
# See https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/core/constants.py for the available choices. Used in various metadata fields.
# Default: None
SITE_LICENSE = None

# Creator of the Daiquiri site. Used in the VO registry entry. Has to be of the following form:
# Default: None
SITE_CREATOR = "LIneA"
SITE_LOGO_URL = "https://linea.org.br/favicon.ico"

# List of contacts for the Daiquiri site. Used in the VO registry entry. Has to be of the following form:
# Default: None
SITE_CONTACT = {
    "name": "LIneA Helpdesk",
    "address": "Rio de Janeiro, Brasil",
    "email": "helpdesk@linea.org.br",
    "telephone": "55 21 96937 9224",
}

# Publisher of the Daiquiri site. Used for VO and OAI metadata.
# Default: None
SITE_PUBLISHER = "LIneA - Laboratório Interinstitucional de e-Astronomia"

# Date of the creation of the Daiquiri site. Used for VO and OAI metadata. Has to be of the form
# Default: None
SITE_CREATED = "2023-04-19"

# Date of the last update of the Daiquiri site. Used for VO and OAI metadata. Has to be of the form
# Default: None
SITE_UPDATED = "2024-06-13"

LINEA_APPS = ["djangosaml2", "services", "data", "utils"]

WAGTAIL_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "wagtailmarkdown",
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
    + WAGTAIL_APPS
)

# -----------------------------------------------
# Wagtail - CMS for custom pages
# https://docs.wagtail.org/en/stable/getting_started/integrating_into_django.html
# -----------------------------------------------
MIDDLEWARE += ("wagtail.contrib.redirects.middleware.RedirectMiddleware",)

# STATIC_ROOT está definido no core do daiquiri
# https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/core/settings/django.py
# STATIC_ROOT = BASE_DIR / 'static_root/'

# STATIC_URL: NÃO ALTERAR: Esta variavel estão relacionada a rota /daiquiri_static/ no ngnix e no uWSGI.
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/daiquiri_static/"

# MEDIA_ROOT está definido no core do daiquiri
# https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/core/settings/django.py#L158
# MEDIA_URL = BASE_URL + 'media/'
# MEDIA_ROOT = BASE_DIR / 'media_root/'

# this will be displayed on the main dashboard of the Wagtail admin backend:
WAGTAIL_SITE_NAME = "LIneA Userquery"

# WAGTAILADMIN_BASE_URL - this is the base URL used by the Wagtail admin site.
# It is typically used for generating URLs to include in notification emails
WAGTAILADMIN_BASE_URL = SITE_URL

# WAGTAILDOCS_EXTENSIONS setting to specify the file types that Wagtail
# will allow to be uploaded as documents.
# https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

# WAGTAIL MARKDOWN
# https://github.com/torchbox/wagtail-markdown
WAGTAILMARKDOWN = {
    "autodownload_fontawesome": True,
    "allowed_tags": [],  # optional. a list of HTML tags. e.g. ['div', 'p', 'a']
    "allowed_styles": [],  # optional. a list of styles
    "allowed_attributes": {},  # optional. a dict with HTML tag as key and a list of attributes as value
    "allowed_settings_mode": "extend",  # optional. Possible values: "extend" or "override". Defaults to "extend".
    "extensions": [
        "extra",
        "abbr",
        "attr_list",
        "def_list",
        "fenced_code",
        "footnotes",
        "md_in_html",
        "tables",
        "admonition",
        "codehilite",
        "legacy_attrs",
        "legacy_em",
        "meta",
        "nl2br",
        "sane_lists",
        "smarty",
        "toc",
        "wikilinks",
    ],  # optional. a list of python-markdown supported extensions
    "extension_configs": {},  # optional. a dictionary with the extension name as key, and its configuration as value
    "extensions_settings_mode": "extend",  # optional. Possible values: "extend" or "override". Defaults to "extend".
    "tab_length": 4,  # optional. Sets the length of tabs used by python-markdown to render the output. This is the number of spaces used to replace with a tab character. Defaults to 4.
}

# -----------------------------------------------


ACCOUNT_EMAIL_VERIFICATION = "none"

# NÃO ALTERAR: Estas variaveis estão relacionadas a rota /protected/ no ngnix.
# São necessárias para o funcionamento do Download.
# https://django-sendfile2.readthedocs.io/en/latest/backends.html#nginx-backend
SENDFILE_BACKEND = "django_sendfile.backends.nginx"
SENDFILE_ROOT = "/data/download/"
SENDFILE_URL = "/download"


# Diretorio onde ficam os arquivos de PID do celery
# Não alterar este path por que ele está sendo utilizado no script start.sh
CELERY_PIDFILE_PATH = "/tmp"


SERVE_DOWNLOAD_DIR = "/data/download"

ANNOUNCEMENT_MESSAGE_FILTER = "linea.filters.LineaMessageFilter"

CONESEARCH_ADAPTER = "daiquiri.conesearch.adapter.SimpleConeSearchAdapter"
CONESEARCH_ANONYMOUS = True
CONESEARCH_SCHEMA = "des_dr2"
CONESEARCH_TABLE = "main"
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

# daiquiri.query.settings
# Sets the timeout for syncronous (TAP) queries in seconds.
# Default: 'daiquiri_user_'
QUERY_USER_SCHEMA_PREFIX = "mydb_"

QUERY_DROPDOWNS = [
    {
        "key": "simbad",
        "service": "query/js/dropdowns/simbad.js",
        "template": "query/query_dropdown_simbad.html",
        "options": {"url": "https://simbad.u-strasbg.fr/simbad/sim-id"},
    },
    {
        "key": "vizier",
        "service": "query/js/dropdowns/vizier.js",
        "template": "query/query_dropdown_vizier.html",
        "options": {
            "url": "https://vizier.u-strasbg.fr/viz-bin/votable",
            "catalogs": [
                "I/322A",
                "I/259",
                "II/281",
                "II/246",
                "V/139",
                "V/147",
                "I/317",
                "II/328/allwise",
                "II/312/ais",
                "I/345",
                "I/350",
                "I/329",
                "II/349",
                "II/342",
            ],
        },
    },
]

QUERY_LANGUAGES = [
    {
        "key": "adql",
        "version": 2.0,
        "label": "ADQL",
        "description": "",
        "quote_char": '"',
    },
    {
        "key": "postgresql",
        "version": 13.9,
        "label": "PostgreSQL",
        "description": "",
        "quote_char": '"',
    },
]

# -----------------------------------------------
# GAIA AIP LICENSE
# https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/metadata/settings.py
# -----------------------------------------------

LICENSE_CHOICES = list(LICENSE_CHOICES)
LICENSE_BY_GAIA = "BY_GAIA"
LICENSE_CHOICES.append((LICENSE_BY_GAIA, _("Gaia Data License")))
LICENSE_URLS[LICENSE_BY_GAIA] = "https://gaia.aip.de/cms/credit/"
LICENSE_IDENTIFIERS[LICENSE_BY_GAIA] = "BY_GAIA"
LICENSE_CHOICES = tuple(LICENSE_CHOICES)


# -----------------------------------------------
# LInea Specific
# -----------------------------------------------
TARGET_VIEWER_URL = "https://scienceserver-dev.linea.org.br/target/"
SCIENCE_SERVER_URL = "https://scienceserver-dev.linea.org.br/"

# COmanage Autorization
COMANAGE_SERVER_URL = env.get("COMANAGE_SERVER_URL", "https://register.linea.org.br")
COMANAGE_USER = env.get("COMANAGE_USER")
COMANAGE_PASSWORD = env.get("COMANAGE_PASSWORD")
COMANAGE_COID = env.get("COMANAGE_COID", 2)

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
        # "eduPersonPrincipalName": ("username",),
        "eduPersonUniqueId": ("username",),
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
            "remote": [
                {
                    "url": "https://www.linea.org.br/static/metadata/satosa-prod-frontend-cilogon.xml",
                    "cert": None,
                },
                {
                    "url": "https://www.linea.org.br/static/metadata/satosa-prod-frontend-cafe.xml",
                    "cert": None,
                },
            ]
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
                "given_name": "Service",
                "sur_name": "Desk",
                "company": "LIneA",
                "email_address": "helpdesk@linea.org.br",
                "contact_type": "technical",
            },
        ],
        # Descreve a organização responsável pelo serviço
        "organization": {
            "name": [("LIneA", "pt-br")],
            "display_name": [("LIneA", "pt-br")],
            "url": [("https://www.linea.org.br", "pt-br")],
        },
    }

SETTINGS_EXPORT += [
    "AUTH_SAML2_ENABLED",
    "LOGIN_URL",
    "LOGOUT_URL",
    "TARGET_VIEWER_URL",
    "SCIENCE_SERVER_URL",
]
