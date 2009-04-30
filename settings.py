import os

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

ADMINS = ()

DATABASE_ENGINE = 'appengine'
AUTH_USER_MODULE = 'ragendja.auth.models'

DJANGO_STYLE_MODEL_KIND = False

INSTALLED_APPS = (
    'appenginepatcher',
    'django.contrib.auth',
    'app',
)

ROOT_URLCONF = 'app.urls'

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
    os.path.join(os.path.dirname(__file__), 'templates'),
    '/base/python_lib/versions/1/google/appengine/ext/admin/templates'
)
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    CACHE_BACKEND = 'dummy:///'
else:
    CACHE_BACKEND = 'memcached://?timeout=300'

