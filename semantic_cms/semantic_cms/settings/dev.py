from .base import *

TEMPLATE_DEBUG = DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'semantic_cms',
        'USER': 'semantic_cms_user',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
