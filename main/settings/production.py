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
    'www.jackalfaction.uk'
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': f'{os.environ["DB_NAME"]}',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
    }
}

try:
    from .local import *
except ImportError:
    pass
