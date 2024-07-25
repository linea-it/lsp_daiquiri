# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = [
    'userquery-dev.linea.org.br:8080', 
    'userquery-dev.linea.org.br', 
    'scienceserver-dev.linea.org.br'
]


QUERY_DROPDOWNS = [
    {
        'key': 'simbad',
        'service': 'query/js/dropdowns/simbad.js',
        'template': 'query/query_dropdown_simbad.html',
        'options': {
            'url': 'https://simbad.u-strasbg.fr/simbad/sim-id'
        }
    },
    {
        'key': 'vizier',
        'service': 'query/js/dropdowns/vizier.js',
        'template': 'query/query_dropdown_vizier.html',
        'options': {
            'url': 'https://vizier.u-strasbg.fr/viz-bin/votable',
            'catalogs': ['I/322A', 'I/259', 'II/281', 'II/246', 'V/139', 'V/147', 'I/317', 'II/328/allwise', 'II/312/ais', 'I/345', 'I/350', 'I/329', 'II/349', 'II/342']
        }
    },
]

QUERY_QUEUES = [
    {
        "key": "default",
        "label": "30 Seconds",
        "timeout": 30,
        "priority": 1,
        "access_level": "PUBLIC",
        "groups": [],
    },
    {
        "key": "five_minutes",
        "label": "5 Minutes",
        "timeout": 300,
        "priority": 2,
        "access_level": "PUBLIC",
        "groups": [],
    },
    {
        "key": "two_hours",
        "label": "Two hours",
        "timeout": 7200,
        "priority": 3,
        "access_level": "PUBLIC",
        "groups": [],
    },
]

QUERY_LANGUAGES = [
    {
        'key': 'adql',
        'version': 2.0,
        'label': 'ADQL',
        'description': '',
        'quote_char': '"'
    },
    {
        'key': 'postgresql',
        'version': 13.9,
        'label': 'PostgreSQL',
        'description': '',
        'quote_char': '"'
    }
]

# daiquiri.query.settings
# Designates if the query interface can be accessed by anonymus users.
# The permissions on schemas and tables need to be configured using the metadata interface.
# Default: False
QUERY_ANONYMOUS = True

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
QUERY_SYNC_TIMEOUT = 300