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

CONESEARCH_ANONYMOUS = True
CONESEARCH_STMT = 'SELECT * FROM daiquiri_data_obs.stars WHERE SQRT(POWER(ra - %(RA)s, 2) + POWER(de - %(DEC)s, 2)) <= %(SR)s'

AUTH_DETAIL_KEYS = []

MEETINGS_PARTICIPANT_DETAIL_KEYS = [
    {
        'key': 'affiliation',
        'label': 'Affiliation',
        'data_type': 'text',
        'required': True
    },
    {
        'key': 'dinner',
        'label': 'Conference dinner',
        'data_type': 'radio',
        'required': True,
        'options': [
            {'id': 'yes', 'label': 'yes'},
            {'id': 'no', 'label': 'no'}
        ]
    }
]

QUERY_QUOTA = {
    'user': '1Gb'
}

VENDOR_CDN = False
