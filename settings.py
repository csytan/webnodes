import os
import lib

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

ADMINS = ()

DATABASE_ENGINE = 'appengine'
AUTHENTICATION_BACKENDS = ('apps.users.models.ModelBackend',)
LOGIN_URL = '/users/login'
ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
### Remember to disable InstallAuthentication() in appengine_django/__init__.py
    'appengine_django',
    'django.contrib.sessions',
    'django.contrib.auth',
    'apps.forum',
    'apps.users',
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

