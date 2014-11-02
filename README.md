# Banyan

## Collaborative social experiences

This is a product being built by the Assembly community. You can help push this idea forward by visiting [https://assembly.com/banyan](https://assembly.com/banyan).

### Getting started

This repo is the backend for [Banyan](www.banyan.io).
- The backend is written in Django and API exposed through Tastypie.
- Celery and Redis are used for async workload and caching.
- PostgreSQL 9.3 for database.
- Amazon S3 for media storage and SNS for push notifications.

To start contributing to this project:

1. Create a virtualenv (recommended) and activate it
2. Clone this git repo at the desired (virtualenv) directory
3. Install the requirements (pip install -r requirements.txt)
4. Create a *banyan/local_settings.py* file and add the configuration at the end of this README
5. Make sure Postgres and Redis (optional to start server, needed for celery) are running
6. Sync the database and migrate apps (`./manage.py syncdb; ./manage.py migrate <apps>`)
7. Run the local server: `./manage.py runserver`
8. Run celery: `celery -A banyan worker -l info -B`

Banyan development webserver is now running!

A sample *banyan/local_settings.py* file:
```
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

# PROJECT DATABASE SETTINGS
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "banyan_dev",
        "HOST": "localhost",
        "PORT": "",
    }
}

# Root address of our site
ROOT = 'http://127.0.0.1:8080'

# Celery configurations
BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_SEND_TASK_ERROR_EMAILS = False
# CELERY_ALWAYS_EAGER = True

#Facebook Connect (Banyan Dev)
SOCIAL_AUTH_FACEBOOK_KEY = 'a facebook key'
SOCIAL_AUTH_FACEBOOK_SECRET = 'a facebook secret'
FACEBOOK_APP_ACCESS_TOKEN = 'facebook app access token'

#AWS Configurations
AWS_ACCESS_KEY_ID = 'aws access key'
AWS_SECRET_ACCESS_KEY = 'aws secret key' 
AWS_STORAGE_BUCKET_NAME = 'dev_banyancdn'

# SNS Configurations
AWS_SNS_APNS_PLATFORM = 'APNS_SANDBOX'
AWS_S3_MEDIA_BUCKET = 'dev_banyancontent'

ALLOWED_HOSTS = [
    '127.0.0.1',
]
INTERNAL_IPS = ALLOWED_HOSTS

REDIS_ENDPOINT = '127.0.0.1'

#  Caching related parameters
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '%s:6379:1' % (REDIS_ENDPOINT),
    }
}

CACHEOPS_REDIS = {
    'host': REDIS_ENDPOINT, # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 1,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended
    'socket_timeout': 3,
}
```
