#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pathlib
import dotenv

def main():
    """Run administrative tasks."""
    if (pathlib.Path()/ ".env").exists():
        dotenv.read_dotenv()  
    else:
        print("no .env file read")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djlexique.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
