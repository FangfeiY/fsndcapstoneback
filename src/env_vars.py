import os

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS")
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL_HEROKU = os.environ.get("DATABASE_URL_HEROKU")
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_API_AUDIENCE = os.environ.get('AUTH0_API_AUDIENCE')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SEC = os.environ.get('AUTH0_CLIENT_SEC')
METEOR_TESTING = True if os.environ.get('METEOR_TESTING').lower() == 'true' else False
