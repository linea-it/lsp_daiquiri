import os

from . import BASE_DIR, INSTALLED_APPS

INSTALLED_APPS += [
    'daiquiri.auth',
    'daiquiri.contact',
    'daiquiri.core',
    'daiquiri.jobs',
    'daiquiri.meetings',
    'daiquiri.metadata',
    'daiquiri.query',
    'daiquiri.serve',
]

ROOT_URLCONF = 'daiquiri_app.urls'

WSGI_APPLICATION = 'daiquiri_app.wsgi.application'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_PASSWORD_MIN_LENGTH = 4

ASYNC = False

LOGGING_DIR = os.path.join(BASE_DIR, 'log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'django': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'django.log'),
            'formatter': 'standard'
        },
        'sql': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'filename': os.path.join(LOGGING_DIR, 'sql.log'),
        },
        'auth': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'auth.log'),
            'formatter': 'standard'
        },
        'rules': {
             'class': 'logging.FileHandler',
             'level': 'DEBUG',
             'filename': os.path.join(LOGGING_DIR, 'rules.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'auth': {
            'handlers': ['console', 'auth'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
        'rules': {
            'handlers': ['rules'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


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

QUERY = {
    'user_database_prefix': 'daiquiri_user_',
    'quota': {
        'users': '10Gb'
    },
    'queues': (
        ['10s', '10 Seconds'],
        ['60s', '1 Minute']
    ),
    'query_languages': (
        ['mysql', 'MySQL SQL'],
        ['adql', 'ADQL'],
    ),
    'forms': [
        {
            'key': 'sql',
            'label': 'SQL query',
            'service': 'query/js/forms/sql.js',
            'template': 'query/query_form_sql.html'
        },
        {
            'key': 'box',
            'label': 'Box search',
            'service': 'query/js/forms/box.js',
            'template': 'query/query_form_box.html'
        },
        {
            'key': 'cone',
            'label': 'Cone search',
            'service': 'query/js/forms/cone.js',
            'template': 'query/query_form_cone.html'
        },
    ],
    'dropdowns': [
        {
            'key': 'simbad',
            'service': 'query/js/dropdowns/simbad.js',
            'template': 'query/query_dropdown_simbad.html',
            'options': {
                'url': 'http://simbad.u-strasbg.fr/simbad/sim-id'
            }
        },
        {
            'key': 'vizier',
            'service': 'query/js/dropdowns/vizier.js',
            'template': 'query/query_dropdown_vizier.html',
            'options': {
                'url': 'http://vizier.u-strasbg.fr/viz-bin/votable',
                'catalogs': ['I/322A', 'I/259']
            }
        }
    ],
    'download_dir': '/store/daiquiri/download/',
    'download_formats': [
        {
            'key': 'csv',
            'extension': 'csv',
            'label': 'Comma separated Values',
            'help': 'A text file with a line for each row of the table. The fields are delimited by a comma and quoted by double quotes. Use this option for a later import into a spreadsheed application or a custom script. Use this option if you are unsure what to use.'
        },
        {
            'key': 'votable',
            'extension': 'votable.xml',
            'label': 'IVOA VOTable XML file - ASCII Format',
            'help': 'A XML file using the IVOA VOTable format. Use this option if you intend to use VO compatible software to further process the data.'
        },
        {
            'key': 'votableB1',
            'extension': 'votable.b1.xml',
            'label': 'IVOA VOTable XML file - BINARY 1 Format',
            'help': 'A XML file using the IVOA VOTable format (BINARY Serialization). Use this option if you intend to use VO compatible software to process the data and prefer the use of a binary file.'
        },
        {
            'key': 'votableB2',
            'extension': 'votable.b2.xml',
            'label': 'IVOA VOTable XML file - BINARY 2 Format',
            'help': 'A XML file using the IVOA VOTable format (BINARY2 Serialization). Use this option if you intend to use VO compatible software to process the data and prefer the use of a binary file.'
        }
    ]
}
