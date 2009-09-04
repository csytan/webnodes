import os
import lib

DEBUG = os.environ.get('SERVER_SOFTWARE', 'Dev').startswith('Dev')

# Appengine patch settings for running manage.py
MEDIA_VERSION = 1
COMBINE_MEDIA = {}

#SESSION_COOKIE_DOMAIN = '.mysite.com'

ADMINS = ()
DATABASE_ENGINE = 'appengine'
DJANGO_STYLE_MODEL_KIND = False

AUTH_USER_MODULE = 'apps.users.models'

LOGIN_URL = '/users/login'
ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.auth',
    'appenginepatcher',
    'apps.core',
    'apps.mail',
    'apps.users',
)

MIDDLEWARE_CLASSES = (
    'apps.core.middleware.SubdomainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
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
    os.path.join(os.path.dirname(__file__), 'templates'),
)
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    CACHE_BACKEND = 'dummy:///'
else:
    CACHE_BACKEND = 'memcached://?timeout=300'

