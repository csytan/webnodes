import os
import sys

import lib

# add lib directory to sys.path for global import
sys.path.append(os.path.dirname(lib.__file__))

# import global libs so they are cached:
# appengine resets sys.path between requests
import feedparser
import markdown2

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

ADMINS = ()

DATABASE_ENGINE = 'appengine'
DJANGO_STYLE_MODEL_KIND = False
AUTH_USER_MODULE = 'apps.users.models'

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.auth',
    'apps.forum',
    'apps.users',
    'appenginepatcher',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    CACHE_BACKEND = 'dummy:///'
else:
    CACHE_BACKEND = 'memcached://?timeout=300'

