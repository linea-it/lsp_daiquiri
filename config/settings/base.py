import os
from . import BASE_DIR

DAIQUIRI_APPS = [
    'daiquiri.archive',
    'daiquiri.auth',
    'daiquiri.conesearch',
    'daiquiri.contact',
    'daiquiri.core',
    'daiquiri.files',
    'daiquiri.jobs',
    'daiquiri.meetings',
    'daiquiri.metadata',
    'daiquiri.oai',
    'daiquiri.query',
    'daiquiri.registry',
    'daiquiri.serve',
    'daiquiri.stats',
    'daiquiri.tap',
    'daiquiri.uws'
]

INSTALLED_APPS = []

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
    os.path.join(BASE_DIR, 'vendor/'),
)

SITE_URL = 'http://localhost:8000'
SITE_IDENTIFIER = 'example.com'
SITE_TITLE = 'example.com'
SITE_DESCRIPTION = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
SITE_LICENSE = 'CC0'
SITE_CREATOR = 'Anna Admin'
SITE_PUBLISHER = 'At vero eos et accusam'
SITE_CREATED = '2019-01-01'
SITE_UPDATED = '2019-04-01'

CONESEARCH_ANONYMOUS = True
QUERY_ANONYMOUS = True

CONESEARCH_SCHEMA = 'daiquiri_data_obs'
CONESEARCH_TABLE = 'stars'
