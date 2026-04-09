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

# Hostname e porta do servidor atual
BASE_HOST = env.get("BASE_HOST", default="http://localhost")

# URL pública do site Daiquiri. Usada em metadados VO e OAI.
# Padrão: http://localhost:8000
SITE_URL = env.get("SITE_URL")

# Identificador do site Daiquiri. Em geral a URL sem o protocolo. Usado em metadados VO e OAI.
# Padrão: None
SITE_IDENTIFIER = env.get("DOMAIN")
# Título do site Daiquiri. Usado em metadados VO e OAI.
# Padrão: None
SITE_TITLE = "LIneA TAP Service"

# Descrição do site Daiquiri. Usada em metadados VO e OAI.
# Padrão: None
SITE_DESCRIPTION = "The TAP Service registry for linea.org.br"

# Licença do site Daiquiri.
# Ver https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/core/constants.py para as opções. Usada em vários campos de metadados.
# Padrão: None
SITE_LICENSE = None

# Criador do site Daiquiri. Usado na entrada do registro VO. Deve seguir o formato indicado na documentação.
# Padrão: None
SITE_CREATOR = "LIneA"
SITE_LOGO_URL = "https://linea.org.br/favicon.ico"

# Lista de contatos do site Daiquiri. Usada na entrada do registro VO. Deve seguir o formato indicado na documentação.
# Padrão: None
SITE_CONTACT = {
    "name": "LIneA Helpdesk",
    "address": "Rio de Janeiro, Brasil",
    "email": "helpdesk@linea.org.br",
    "telephone": "55 21 96937 9224",
}

# Editora do site Daiquiri. Usada em metadados VO e OAI.
# Padrão: None
SITE_PUBLISHER = "LIneA - Laboratório Interinstitucional de e-Astronomia"

# Data de criação do site Daiquiri. Usada em metadados VO e OAI. Formato conforme documentação.
# Padrão: None
SITE_CREATED = "2023-04-19"

# Data da última atualização do site Daiquiri. Usada em metadados VO e OAI. Formato conforme documentação.
# Padrão: None
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
# Wagtail — CMS para páginas customizadas
# https://docs.wagtail.org/en/stable/getting_started/integrating_into_django.html
# -----------------------------------------------
MIDDLEWARE += ("wagtail.contrib.redirects.middleware.RedirectMiddleware",)

# STATIC_ROOT está definido no core do daiquiri
# https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/core/settings/django.py
# STATIC_ROOT = BASE_DIR / 'static_root/'

# STATIC_URL: NÃO ALTERAR — relacionada à rota /daiquiri_static/ no Nginx e no uWSGI.
# Arquivos estáticos (CSS, JavaScript, imagens)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/daiquiri_static/"

# Logos/banners LINEA em <BASE_DIR>/static/daiquiri/ (fora de uma app com static/)
STATICFILES_DIRS = [BASE_DIR / "static"]

# MEDIA_ROOT está definido no core do daiquiri
# https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/core/settings/django.py#L158
# MEDIA_URL = BASE_URL + 'media/'
# MEDIA_ROOT = BASE_DIR / 'media_root/'

# Nome exibido no painel principal do admin Wagtail
WAGTAIL_SITE_NAME = "LIneA Userquery"

# WAGTAILADMIN_BASE_URL — URL base usada pelo site de administração Wagtail.
# Em geral usada para gerar URLs em e-mails de notificação
WAGTAILADMIN_BASE_URL = SITE_URL

# WAGTAILDOCS_EXTENSIONS — tipos de arquivo que o Wagtail permite enviar como documentos.
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
    "allowed_tags": [],  # opcional: lista de tags HTML, ex.: ['div', 'p', 'a']
    "allowed_styles": [],  # opcional: lista de estilos
    "allowed_attributes": {},  # opcional: dict com tag HTML como chave e lista de atributos como valor
    "allowed_settings_mode": "extend",  # opcional: "extend" ou "override". Padrão: "extend".
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
    ],  # opcional: extensões suportadas pelo python-markdown
    "extension_configs": {},  # opcional: dict nome da extensão → configuração
    "extensions_settings_mode": "extend",  # opcional: "extend" ou "override". Padrão: "extend".
    "tab_length": 4,  # opcional: largura da tabulação usada pelo python-markdown (espaços). Padrão: 4.
}

# -----------------------------------------------


ACCOUNT_EMAIL_VERIFICATION = "none"

# NÃO ALTERAR: estas variáveis estão relacionadas à rota /protected/ no Nginx.
# São necessárias para o funcionamento do Download.
# https://django-sendfile2.readthedocs.io/en/latest/backends.html#nginx-backend
SENDFILE_BACKEND = "django_sendfile.backends.nginx"
SENDFILE_ROOT = "/data/download/"
SENDFILE_URL = "/download"


# Diretório dos arquivos PID do Celery
# Não alterar: o caminho é usado pelo script start.sh
CELERY_PIDFILE_PATH = "/tmp"


SERVE_DOWNLOAD_DIR = "/data/download"

ANNOUNCEMENT_MESSAGE_FILTER = "linea.filters.LineaMessageFilter"

CONESEARCH_ADAPTER = "daiquiri.conesearch.adapter.SimpleConeSearchAdapter"

# Adaptador PostgreSQL customizado: colunas numeric/decimal são descobertas
# como tipo TAP 'double' em vez de 'char' (ver linea.adapter).
ADAPTER_DATABASE = "linea.adapter.PostgreSQLAdapter"

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
# Define o prefixo do schema de usuário para jobs de query (não é timeout; ver documentação do pacote).
# Padrão típico: 'mydb_' ou 'daiquiri_user_'
QUERY_USER_SCHEMA_PREFIX = "mydb_"

# Barra do FormSql (1.3+): cada key precisa estar definida aqui (incl. examples, schemas, …).
QUERY_DROPDOWNS = [
    {"key": "schemas", "label": "Database"},
    {"key": "columns", "label": "Columns"},
    {"key": "functions", "label": "Functions"},
    {
        "key": "simbad",
        "label": "Simbad",
        "service": "query/js/dropdowns/simbad.js",
        "template": "query/query_dropdown_simbad.html",
        "options": {"url": "https://simbad.u-strasbg.fr/simbad/sim-id"},
    },
    {
        "key": "vizier",
        "label": "VizieR",
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
    {"key": "examples", "label": "Examples", "classes": "ms-auto"},
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
        "version": 18.1,
        "label": "PostgreSQL",
        "description": "",
        "quote_char": '"',
    },
]

# -----------------------------------------------
# Licença Gaia AIP
# https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/metadata/settings.py
# -----------------------------------------------

LICENSE_CHOICES = list(LICENSE_CHOICES)
LICENSE_BY_GAIA = "BY_GAIA"
LICENSE_CHOICES.append((LICENSE_BY_GAIA, _("Gaia Data License")))
LICENSE_URLS[LICENSE_BY_GAIA] = "https://gaia.aip.de/cms/credit/"
LICENSE_IDENTIFIERS[LICENSE_BY_GAIA] = "BY_GAIA"
LICENSE_CHOICES = tuple(LICENSE_CHOICES)


# -----------------------------------------------
# Específico da LIneA
# -----------------------------------------------
TARGET_VIEWER_URL = "https://scienceserver-dev.linea.org.br/target/"
SCIENCE_SERVER_URL = "https://scienceserver-dev.linea.org.br/"
LSP_URL = "https://scienceplatform-dev.linea.org.br/lsp"
IDAC_URL = "https://scienceplatform-dev.linea.org.br/idac"

# # Autorização COmanage
# COMANAGE_SERVER_URL = env.get("COMANAGE_SERVER_URL", "https://register.linea.org.br")
# COMANAGE_USER = env.get("COMANAGE_USER")
# COMANAGE_PASSWORD = env.get("COMANAGE_PASSWORD")
# COMANAGE_COID = env.get("COMANAGE_COID", 2)

# Autenticação Django SAML2
AUTH_SAML2_ENABLED = env.get_bool("AUTH_SAML2_ENABLED", False)

# URLs de login com SAML2/CILogon
# Exemplo URL_CILOGON: https://skyviewer.linea.org.br/saml2/login/?idp=https://satosa.linea.org.br/linea/proxy/aHR0cHM6Ly9jaWxvZ29uLm9yZw==
LINEA_LOGIN_URL = env.get("LINEA_LOGIN_URL", default="/admin/login/?next=/")
RUBIN_LOGIN_URL = env.get("RUBIN_LOGIN_URL", default="/admin/login/?next=/")

# URL de registro para os diferentes IdPs.
LINEA_REGISTER_URL = env.get(
    "LINEA_REGISTER_URL",
    default="https://register-dev.linea.org.br/Shibboleth.sso/Login?SAMLDS=1&target=https://register-dev.linea.org.br/registry/co_petitions/start/coef:155&entityID=https://satosa.linea.org.br/linea/proxy/aHR0cHM6Ly9jaWxvZ29uLm9yZw==",
)
RUBIN_REGISTER_URL = env.get(
    "RUBIN_REGISTER_URL",
    default="https://register-dev.linea.org.br/Shibboleth.sso/Login?SAMLDS=1&target=https://register-dev.linea.org.br/registry/co_petitions/start/coef:231&entityID=https://satosa-dev.linea.org.br/linea_saml_mirror/proxy/aHR0cHM6Ly9kYXRhLmxzc3QuY2xvdWQ=",
)

# Lista de grupos internos do sistema.
# Esses grupos são gerenciados no Django admin.
# Quando o usuário faz login pelo SAML2, esses grupos não serão removidos.
INTERNAL_GROUPS = [
    "Editors",
    "Moderators",
    "contact_manager",
    "metadata_manager",
    "query_manager",
    "stats_manager",
    "user_manager",
]

if AUTH_SAML2_ENABLED == True:

    # DOMAIN — exemplo: userquery-dev.linea.org.br
    DOMAIN = env.get("DOMAIN")

    # FQDN — exemplo: https://userquery-dev.linea.org.br
    FQDN = env.get("SITE_URL")
    # FQDN = "https://" + DOMAIN
    CERT_DIR = "certificates"

    # Backend de autenticação SAML2 (inclusão)
    # AUTHENTICATION_BACKENDS += ("djangosaml2.backends.Saml2Backend", )
    # Backend SAML2 customizado da LIneA
    AUTHENTICATION_BACKENDS += ("linea.saml2.LineaSaml2Backend",)
    # Middleware SAML2
    MIDDLEWARE += ("djangosaml2.middleware.SamlSessionMiddleware",)
    # Tratamento customizado de falha no ACS SAML2
    # https://djangosaml2.readthedocs.io/contents/developer.html#custom-error-handler
    SAML_ACS_FAILURE_RESPONSE_FUNCTION = "linea.views.saml2_template_failure"
    # Configurações do cookie de sessão
    SAML_SESSION_COOKIE_NAME = "saml_session"
    SESSION_COOKIE_SECURE = True

    # Qualquer view que exige usuário autenticado redireciona o navegador para esta URL
    LOGIN_URL = "/login/"

    # Encerra a sessão quando o usuário fecha o navegador
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False

    # Tipo de binding utilizado
    SAML_DEFAULT_BINDING = saml2.BINDING_HTTP_POST
    SAML_IGNORE_LOGOUT_ERRORS = True

    # Serviço de descoberta da cafeexpresso (RNP)
    # SAML2_DISCO_URL = 'https://ds.cafeexpresso.rnp.br/WAYF.php'

    # Cria usuário Django a partir da asserção SAML se ainda não existir
    SAML_CREATE_UNKNOWN_USER = True

    # https://djangosaml2.readthedocs.io/contents/security.html#content-security-policy
    SAML_CSP_HANDLER = ""

    # URL para redirecionamento após a autenticação
    LOGIN_REDIRECT_URL = "/query"

    SAML_ATTRIBUTE_MAPPING = {
        "eduPersonUniqueId": ("username",),
        "cn": ("first_name",),
        "sn": ("last_name",),
        "email": ("email",),
        # "isMemberOf": ("name",),
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
                    "url": "https://www.linea.org.br/static/metadata/satosa-prod-frontend-rubin.xml",
                    "cert": None,
                },
                {
                    "url": "https://www.linea.org.br/static/metadata/satosa-dev-frontend-cilogon.xml",
                    "cert": None,
                },
                {
                    "url": "https://www.linea.org.br/static/metadata/satosa-dev-frontend-rubin.xml",
                    "cert": None,
                },
            ],
        },
        # 1 = mais informações de depuração
        "debug": 1,
        # Assinatura
        "key_file": os.path.join(BASE_DIR, CERT_DIR, "mykey.pem"),  # chave privada
        "cert_file": os.path.join(
            BASE_DIR, CERT_DIR, "mycert.pem"
        ),  # certificado público
        # Criptografia
        "encryption_keypairs": [
            {
                "key_file": os.path.join(
                    BASE_DIR, CERT_DIR, "mykey.pem"
                ),  # chave privada
                "cert_file": os.path.join(
                    BASE_DIR, CERT_DIR, "mycert.pem"
                ),  # certificado público
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
    "BASE_HOST",
    "AUTH_SAML2_ENABLED",
    "LOGIN_URL",
    "LOGOUT_URL",
    "TARGET_VIEWER_URL",
    "SCIENCE_SERVER_URL",
    "LSP_URL",
    "IDAC_URL",
    "LINEA_LOGIN_URL",
    "LINEA_REGISTER_URL",
    "RUBIN_LOGIN_URL",
    "RUBIN_REGISTER_URL",
]
