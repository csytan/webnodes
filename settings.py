import os

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

ADMINS = ()

DATABASE_ENGINE = 'appengine'
DJANGO_STYLE_MODEL_KIND = False
AUTH_USER_MODULE = 'ragendja.auth.models'

ROOT_URLCONF = 'app.urls'

INSTALLED_APPS = (
    'appenginepatcher',
    'django.contrib.sessions',
    'django.contrib.auth',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = ()
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    CACHE_BACKEND = 'dummy:///'
else:
    CACHE_BACKEND = 'memcached://?timeout=300'

