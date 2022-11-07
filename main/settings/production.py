import os
import dotenv

from .base import *

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']
PAYPAL_CLIENT_ID = os.environ['PAYPAL_CLIENT_ID']

ALLOWED_HOSTS = [
    'jackalsfaction.pythonanywhere.com',
    'jackalfaction.com'
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
