# Django settings for Banyan project.
import os, os.path
import logging
import urllib, urlparse
import dj_database_url

from datetime import timedelta

logging.basicConfig()

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

# Root address of our site
ROOT = 'https://www.banyan.io'

PROJECT_ROOT = os.path.dirname(__file__)

# PROJECT DATABASE SETTINGS
DATABASES = {'default': dj_database_url.config()}

ADMINS = (
    ('Devang Mundhra', 'devang.mundhra@banyan.io'),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MANAGERS = ADMINS
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "https://s3.amazonaws.com/banyancdn/"

# Additional locations of static files
STATICFILES_DIRS = (
#    os.path.join(PROJECT_ROOT, "static/"),
    os.path.join(PROJECT_ROOT, "media/"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Custom user models
AUTH_USER_MODEL = 'accounts.BanyanUser'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-ijcxhpr4u243km60nv-%v1=q+y+1eyhqjd1#@%9n9g-^s53h('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MODELTRANSLATION_TRANSLATION_REGISTRY = "banyan.translation"

# template context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#     'core.middleware.ProfileMiddleware', #Used for profiling, use only in dev server
)

COMBINED_INBOX_COUNT_SOURCES = [
    "messages.context_processors.inbox",
]

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.RemoteUserBackend',
)

# AUTH_USER_MODEL = 'accounts.BanyanUser'
# SOCIAL_AUTH_USER_MODEL = 'accounts.BanyanUser'
ROOT_URLCONF = 'banyan.urls'

# template directories
TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PROJECT_ROOT, "templates", "banyan")
    #sys.path.insert( 0, abspath( join( PROJECT_ROOT, 'templates' ) ) )
]

# Caching related parameters
if 'REDISCLOUD_URL' in os.environ:
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '%s:%s:0' % (redis_url.hostname, redis_url.port),
            'OPTIONS': {
                'PASSWORD': redis_url.password,
                'DB': 0,
            }
        }
    }
    
    CACHEOPS_REDIS = {
        'host': redis_url.hostname, # redis-server is on same machine
        'port': redis_url.port,        # default redis port
        'db': 0,             # TODO: SELECT non-default redis database
                             # using separate redis db or redis instance
                             # is highly recommended
        'password': redis_url.password,
        'socket_timeout': 3,
    }

# Enable the session parameters once the mobile app is modified
# such that an unsuccessful login signs out of the app
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_CACHE_ALIAS = 'default'
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS = {
            'tastypie.*' : ('get', 60*60*24*365), # 1 year timeout
            'social.*' : ('get', 60*60), # 1 hour timeout for social auth data
            
#             'accounts.banyanuser': ('all', 60*60*24*365), # 1 year timeout
            'core.activity' : ('all', 60*60*24*365), # 1 year timeout
#             'core.story' : ('all', 60*60*24*365), # 1 year timeout
#             'core.piece' : ('all', 60*60*24*365), # 1 year timeout
#             'content_feedback.*' : ('all', 60*60*24*365), # 1 year timeout
#             'access_groups.groupmembership' : ('all', 60*60*24*365), # 1 year timeout
#             'access_groups.sologroupdesc' : ('all', 60*60*24*365), # 1 year timeout
#             'access_groups.fbfriendsofgroupdesc' : ('all', 60*60*24*365), # 1 year timeout
#             'access_groups.publicgroupdesc' : ('all', 60*60*24*365), # 1 year timeout
            # We don't want to cache *.* because that is causing story access groups to be improperly cached
            # Example, in one run, the permittedGroups for a story were coming out to be wrong.
            # So don't cache access_groups.accessgroup
#             '*.*' : ('all', 60*60*24*365), # 1 year timeout
}

INSTALLED_APPS = (
    #base Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # global apps
    'cacheops',

    # project apps
    'accounts',
    'core',
    'access_groups',
    'content_feedback',

    # third party apps
    'tastypie',
    'sorl.thumbnail',
    'social.apps.django_app.default',
    'south',
    'facebook',
    'storages',
    'django_ses',
    'debug_toolbar',
)

# Social Auth setting
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_EXPIRATION = 'expires'
# Protected fields means those values don't get updated (protected from social auth)
SOCIAL_AUTH_PROTECTED_USER_FIELDS = []
if 'FACEBOOK_KEY' in os.environ:
    SOCIAL_AUTH_FACEBOOK_KEY = os.environ['FACEBOOK_KEY']
if 'FACEBOOK_SECRET' in os.environ:
    SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['FACEBOOK_SECRET']
if 'FACEBOOK_APP_ACCESS_TOKEN' in os.environ:
    FACEBOOK_APP_ACCESS_TOKEN = os.environ['FACEBOOK_APP_ACCESS_TOKEN']
FACEBOOK_REDIRECT_URI = 'https://www.banyan.io'
FACEBOOK_CACHE_TIMEOUT = 1800
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile ', 'email', 'user_friends']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# APP SETTINGS
API_DEFAULT_ITEMS_PER_PAGE = 9
LIST_IMAGE_MAX_HEIGHT = 500 # Used as a baseline for creating a random sized thumbnail for the landing page
LIST_IMAGE_MIN_HEIGHT = 200

LOGIN_URL = "home_view"
LOGIN_REDIRECT_URLNAME = "home_view"
LOGIN_REDIRECT_URL = "home_view"
LOGIN_ERROR_URL = "home_view"

# AWS settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

if 'AWS_ACCESS_KEY_ID' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
if 'AWS_SECRET_ACCESS_KEY' in os.environ:
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'] 
AWS_STORAGE_BUCKET_NAME = 'banyancdn'
# SNS Configurations
AWS_SNS_APNS_PLATFORM = 'APNS'

#S3 Configurations
AWS_S3_MEDIA_BUCKET = 'banyanusercontent'
# SES Configurations
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

CONTACT_EMAIL = 'help@banyan.io'
SITE_NAME = 'Banyan'
SERVER_EMAIL = 'devang.mundhra@banyan.io'
EMAIL_BACKEND = 'django_ses.SESBackend'

# Celery configurations
try:
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    BROKER_URL = 'redis://:%s@%s:%s/0' % (redis_url.password, redis_url.hostname, redis_url.port)
except:
    BROKER_URL = 'sqs://'
CELERY_SEND_TASK_ERROR_EMAILS = True
MAILER_EMAIL_BACKEND = 'django_ses.SESBackend'


CELERY_TASK_PUBLISH_RETRY_POLICY = {
    'max_retries': 15,
    'interval_start': 1,
    'interval_step': 10,
    'interval_max': 3600,
}
CELERY_TASK_SERIALIZER = "pickle"

# En/Decryption Sixteen byte key
OBFUSCATE_KEY = b'Sixteen byte key'

WSGI_APPLICATION = 'banyan.wsgi.application'

ALLOWED_HOSTS = [
    '*',
    '.banyan.io', # Allow domain and subdomains
    '.banyan.io.', # Also allow FQDN and subdomains
    'localhost',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django_ses.SESBackend',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
         'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'core': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'utils': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'content_feedback': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

try:
    from local_settings import *
except ImportError, e:
    pass
