# the hostname and port number of the current Server
BASE_HOST = "http://localhost"

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "::1", "*"]

# Public URL of the Daiquiri site. Used for VO and OAI metadata.
# Default: http://localhost:8000
SITE_URL = "http://localhost"

# Identifier for the Daiquiri site. Usually the URL without the protocol. Used for VO and OAI metadata.
# Default: None
SITE_IDENTIFIER = "daiquiri.com"

# The title for the Daiquiri site. Used for VO and OAI metadata.
# Default: None
SITE_TITLE = "LIneA TAP Service"

# The description for the Daiquiri site. Used for VO and OAI metadata.
# Default: None
SITE_DESCRIPTION = "The TAP Service registry for linea.org.br"

# A license for the Daiquiri site. See https://github.com/django-daiquiri/daiquiri/blob/master/daiquiri/core/constants.py for the available choices. Used in various metadata fields.
# Default: None
SITE_LICENSE = None

# Creator of the Daiquiri site. Used in the VO registry entry. Has to be of the following form:
# Default: None
SITE_CREATOR = "LIneA"
SITE_LOGO_URL = "https://scienceserver.linea.org.br/favicon.png"

# List of contacts for the Daiquiri site. Used in the VO registry entry. Has to be of the following form:
# Default: None
SITE_CONTACT = {
    "name": "LIneA Helpdesk",
    "address": "Rio de Janeiro, Brasil",
    "email": "helpdesk@linea.org.br",
    "telephone": "",
}

# Publisher of the Daiquiri site. Used for VO and OAI metadata.
# Default: None
SITE_PUBLISHER = "LIneA - Laboratório Interinstitucional de e-Astronomia"

# Date of the creation of the Daiquiri site. Used for VO and OAI metadata. Has to be of the form
# Default: None
SITE_CREATED = "2023-04-19"

# Date of the last update of the Daiquiri site. Used for VO and OAI metadata. Has to be of the form
# Default: None
SITE_UPDATED = "2023-04-19"

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

# daiquiri.query.settings
# Designates if the query interface can be accessed by anonymus users.
# The permissions on schemas and tables need to be configured using the metadata interface.
# Default: False
QUERY_ANONYMOUS = True

# daiquiri.query.settings
# Sets the timeout for syncronous (TAP) queries in seconds.
# Default: 'daiquiri_user_'
QUERY_USER_SCHEMA_PREFIX = "mydb_"

# daiquiri.query.settings
# Sets the maximum quota for tables in a user’s personal schema.
# The quota need to be set for the anonymous user as well as regular loggen in users (user).
# Additionally, users or groups can be asigned individual quotas, e.g.:
QUERY_QUOTA = {
    "anonymous": "1Gb",
    "user": "10000Mb",
    "users": {"admin": "1000Gb"},
    "groups": {"collab": "100Gb"},
}

# daiquiri.query.settings
# Sets the timeout for syncronous (TAP) queries in seconds.
# Default: 5
QUERY_SYNC_TIMEOUT = 120

# daiquiri.query.settings
# Set the different queue, which can be selected by the users.
# Each queue is represented by a dictionary where:
QUERY_QUEUES = [
    {
        "key": "default",
        "label": "30 Seconds",
        "timeout": 30,
        "concurency": 1,
        "priority": 1,
        "access_level": "PUBLIC",
        "groups": [],
    },
    {
        "key": "five_minutes",
        "label": "5 Minutes",
        "timeout": 300,
        "priority": 2,
        "concurency": 5,
        "access_level": "PUBLIC",
        "groups": [],
    },
    {
        "key": "fifteen_minutes",
        "label": "15 Minutes",
        "timeout": 900,
        "concurency": 5,
        "priority": 3,
        "access_level": "PUBLIC",
        "groups": [],
    },
]

# STATS_RESOURCE_TYPES = [
#     {
#         'key': 'ARCHIVE_DOWNLOAD',
#         'label': 'Archive downloads'
#     },
#     {
#         'key': 'CONESEARCH',
#         'label': 'Performed cone searches'
#     },
#     {
#         'key': 'CUTOUT',
#         'label': 'Performed cutouts'
#     },
#     {
#         'key': 'FILE',
#         'label': 'File downloads'
#     },
#     {
#         'key': 'QUERY',
#         'label': 'Queries'
#     }
# ]

# Setado no .env
# QUERY_DEFAULT_DOWNLOAD_FORMAT
# QUERY_UPLOAD
# QUERY_UPLOAD_LIMIT
