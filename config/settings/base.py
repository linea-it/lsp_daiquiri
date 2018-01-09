DAIQUIRI_APPS = [
    'daiquiri.archive',
    'daiquiri.auth',
    'daiquiri.contact',
    'daiquiri.core',
    'daiquiri.files',
    'daiquiri.jobs',
    'daiquiri.meetings',
    'daiquiri.metadata',
    'daiquiri.query',
    'daiquiri.serve',
    'daiquiri.stats',
    'daiquiri.tap',
    'daiquiri.uws'
]

INSTALLED_APPS = []

ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_PASSWORD_MIN_LENGTH = 4

ADAPTER_DATABASE = 'daiquiri.core.adapter.database.mariadb.MariaDBAdapter'
ADAPTER_DOWNLOAD = 'daiquiri.core.adapter.download.mysqldump.MysqldumpAdapter'

AUTH_DETAIL_KEYS = []

QUERY_QUOTA = {
    'user': '1Gb'
}

QUERY_QUEUES = [
    {
        'key': '30s',
        'label': '30 Seconds',
        'timeout': 30,
        'priority': 5
    },
    {
        'key': '10m',
        'label': '10 Minutes',
        'timeout': 600,
        'priority': 3
    }
]

QUERY_LANGUAGES = [
    {
        'key': 'mariadb',
        'version': 10.1,
        'label': 'MariaDB SQL',
        'description': '',
        'quote_char': '`'
    },
    {
        'key': 'adql',
        'version': 2.0,
        'label': 'ADQL',
        'description': '',
        'quote_char': '"'
    }
]

VENDOR_CDN = False
