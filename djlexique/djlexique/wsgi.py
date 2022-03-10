"""
WSGI config for djlexique project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


def read_env():
    """Configure environment

    Raises:
        ImproperlyConfigured:
    """
    import pathlib

    import dotenv
    from django.core.exceptions import ImproperlyConfigured

    envfile = pathlib.Path().parent / ".env"
    if not envfile.exists():
        msg = f"no '.env' file in {envfile.parent.resolve()}"
        print(msg)
        raise ImproperlyConfigured(msg)
    else:
        dotenv.read_dotenv(dotenv=envfile)


read_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djlexique.settings")

application = get_wsgi_application()
