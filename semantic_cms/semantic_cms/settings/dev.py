from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'semantic_cms',
#         'USER': 'semantic_cms_user',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "semantic_cms.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025

# TEMPLATE_DIRS = (
#     '/Users/tomasmikula/Projects/Semantic-CMS/semantic_cms/templates/',
# )
#
# STATICFILES_DIRS = (
#     '/Users/tomasmikula/Projects/Semantic-CMS/semantic_cms/static',
# )
#
# # MEDIA_DIRS = (
# #     '/Users/tomasmikula/Projects/Semantic-CMS/semantic_cms/media',
# # )
#
# MEDIA_ROOT = '/Users/tomasmikula/Projects/Semantic-CMS/semantic_cms/media'
# MEDIA_URL = '/Users/tomasmikula/Projects/Semantic-CMS/semantic_cms/media/'
