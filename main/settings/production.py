import dotenv

from .base import *

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

try:
    from .local import *
except ImportError:
    pass
