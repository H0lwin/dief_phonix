"""
WSGI config for Phonix Dashboard project.

Exposes the WSGI callable as a module-level variable named ``application``.
Configured for production deployment with Gunicorn.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
import logging
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

logger = logging.getLogger(__name__)

try:
    application = get_wsgi_application()
except Exception as e:
    logger.error(f"Failed to initialize WSGI application: {e}", exc_info=True)
    raise

def application_with_logging(environ, start_response):
    """Wrapper to add request logging"""
    try:
        return application(environ, start_response)
    except Exception as e:
        logger.error(f"WSGI error: {e}", exc_info=True)
        raise
