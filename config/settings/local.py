SECRET_KEY = 'uox6miphiewahx3aegh0uu5Meiceb2phee9johCheeloh9Yoh8weiX1aeGaash9o'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

ASYNC = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'daiquiri_app',
        'USER': 'daiquiri_app',
        'PASSWORD': 'daiquiri_app',
        'HOST': 'localhost'
    },
    'tap': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TAP_SCHEMA',
        'USER': 'daiquiri_tap',
        'PASSWORD': 'daiquiri_tap',
        'HOST': 'localhost'
    },
    'data': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'daiquiri_data',
        'PASSWORD': 'daiquiri_data',
        'HOST': 'localhost'
    }
}

SENDFILE_BACKEND = 'sendfile.backends.development'
