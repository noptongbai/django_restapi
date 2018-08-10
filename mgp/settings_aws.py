from settings import *


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': 'mgp_aws',
        'ENGINE': 'sqlserver',
        'HOST': 'localhost',
        'USER': 'sa',
        'PASSWORD': 'Passw0rd',
        'OPTIONS': {
            'provider': 'SQLNCLI11',
            'use_legacy_date_fields': True,
        }
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
