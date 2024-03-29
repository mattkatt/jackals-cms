#!/usr/bin/env python
import os
import sys
import dotenv

dotenv_file = os.path.join(".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

if __name__ == "__main__":
    if 'IS_DEV' in os.environ and os.environ['IS_DEV'] is True:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
