"""
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from iepy.webui.webui.settings import *

IEPY_VERSION = '0.9.4'
IEPY_LANG = 'en'
SECRET_KEY = 'y3v(707=8gy!92)@ln_&w4s0$yq%2$@p+&bo=w*nd&h^pz@s9*'
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/ezequiel/Documentos/lenguaje_natural/pln-2015/voting/voting_db.sqlite',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangular',
    'corpus',
    'relatives',
    'relatedwidget',
    'voting.webapp',
)
