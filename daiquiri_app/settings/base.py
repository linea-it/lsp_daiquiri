import os

from . import BASE_DIR

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
    'anonymous': True,
    'user_database_prefix': 'daiquiri_user_',
    'quota': {
        'users': '10Gb'
    },
    'queues': [
        {
            'key': '10s',
            'label': '10 Seconds',
            'timeout': 10,
            'priority': 1
        },
        {
            'key': '1m',
            'label': '1 Minute',
            'timeout': 60,
            'priority': 2
        }
    ],
    'query_languages': [
        {
            'key': 'mariadb',
            'version': 10.1,
            'label': 'MariaDB SQL',
            'description': 'The SQL dialect used by MariaDB 10.1'
        },
        {
            'key': 'adql',
            'version': 2.0,
            'label': 'ADQL',
            'description':  'The IVOA Astronomical Data Query Language. Version 2.0'
        }
    ],
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
            'content_type': 'text/csv',
            'label': 'Comma separated Values',
            'help': 'A text file with a line for each row of the table. The fields are delimited by a comma and quoted by double quotes. Use this option for a later import into a spreadsheed application or a custom script. Use this option if you are unsure what to use.'
        },
        {
            'key': 'votable',
            'extension': 'votable.xml',
            'content_type': 'application/xml',
            'label': 'IVOA VOTable XML file - TABLEDATA serialization',
            'help': 'A XML file using the IVOA VOTable format. Use this option if you intend to use VO compatible software to further process the data.'
        },
        {
            'key': 'votable-binary',
            'extension': 'votable.binary.xml',
            'content_type': 'application/xml',
            'label': 'IVOA VOTable XML file - BINARY serialization',
            'help': 'A XML file using the IVOA VOTable format (BINARY Serialization). Use this option if you intend to use VO compatible software to process the data and prefer the use of a binary file.'
        },
        {
            'key': 'votable-binary2',
            'extension': 'votable.binary2.xml',
            'content_type': 'application/xml',
            'label': 'IVOA VOTable XML file - BINARY 2 serialization',
            'help': 'A XML file using the IVOA VOTable format (BINARY2 Serialization). Use this option if you intend to use VO compatible software to process the data and prefer the use of a binary file.'
        }
    ]
}

UWS = {
    'resources': [
        {
            'prefix': r'query',
            'viewset': 'daiquiri.query.viewsets.AsyncQueryJobViewSet',
            'base_name': 'uws_query'
        }
    ]
}
