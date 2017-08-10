# include settimgs from daiquiri
from daiquiri.core.settings.base import *

# include settings from base.py
from .base import *

# include settings from local.py
from .local import *

# include 3rd party apps after the daiquiri apps from base.py
INSTALLED_APPS = DJANGO_APPS + DAIQUIRI_APPS + ADDITIONAL_APPS + INSTALLED_APPS

# include logging settings from logging.py
from daiquiri.core.settings.logging import get_logging_settings
LOGGING = get_logging_settings(LOGGING_DIR)

# prepend the local.BASE_URL to the different URL settings
try:
    LOGIN_URL = BASE_URL + LOGIN_URL
    LOGIN_REDIRECT_URL = BASE_URL + LOGIN_REDIRECT_URL
    LOGOUT_URL = BASE_URL + LOGOUT_URL
    ACCOUNT_LOGOUT_REDIRECT_URL = BASE_URL
    MEDIA_URL = BASE_URL + MEDIA_URL
    STATIC_URL = BASE_URL + STATIC_URL

    CSRF_COOKIE_PATH = BASE_URL + '/'
    LANGUAGE_COOKIE_PATH = BASE_URL + '/'
    SESSION_COOKIE_PATH = BASE_URL + '/'
except NameError:
    pass
