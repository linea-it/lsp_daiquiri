DAIQUIRI_APPS = [
    'daiquiri.auth',
    'daiquiri.contact',
    'daiquiri.core',
    'daiquiri.dali',
    'daiquiri.jobs',
    'daiquiri.meetings',
    'daiquiri.metadata',
    'daiquiri.query',
    'daiquiri.serve',
    'daiquiri.tap',
    'daiquiri.uws'
]

INSTALLED_APPS = []

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_PASSWORD_MIN_LENGTH = 4

ADAPTER_DATABASE = 'daiquiri.core.adapter.database.mariadb.MariaDBAdapter'
ADAPTER_DOWNLOAD = 'daiquiri.core.adapter.download.mysqldump.MysqldumpAdapter'

AUTH = {
    'detail_keys': [
        {
            'key': 'gender',
            'label': 'Gender',
            'data_type': 'radio',
            'help_text': 'The gender you identify with.',
            'options': [
                {
                    'id': 'female',
                    'label': 'Female'
                },
                {
                    'id': 'male',
                    'label': 'Male'
                },
                {
                    'id': 'other',
                    'label': 'Other'
                },
                {
                    'id': 'prefer_not_to_say',
                    'label': 'Prefer not to say'
                }
            ],
            'required': True
        }
    ]
}

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
