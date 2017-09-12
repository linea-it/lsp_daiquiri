SECRET_KEY = 'this is not a very secret key'

DEBUG = False

ASYNC = False

ALLOWED_HOSTS = ['localhost', 'ip6-localhost', '127.0.0.1', '[::1]']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'daiquiri_app',
        'USER': 'daiquiri_app',
        'PASSWORD': 'daiquiri_app'
    },
    'tap': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TAP_SCHEMA',
        'USER': 'daiquiri_tap',
        'PASSWORD': 'daiquiri_tap',
        'HOST': ''
    },
    'data': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'daiquiri_data',
        'PASSWORD': 'daiquiri_data',
        'HOST': ''
    }
}

# BASE_URL = ''

# AUTH_WORKFLOW = 'confirmation'
# AUTH_WORKFLOW = 'activation'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '25'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True

# SENDFILE_BACKEND = 'sendfile.backends.development'
