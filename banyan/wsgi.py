"""
WSGI config for banyan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banyan.settings")

from os.path import abspath, dirname, join
from site import addsitedir

# Appending the path instead of inserting since there are some module (like celery)
# which we would like Django to pick up from the absolute_path (not the project path)
ROOT = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(ROOT)
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(PROJECT_ROOT)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
