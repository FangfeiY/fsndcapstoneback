import os

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS")
DATABASE_URL = os.environ.get("DATABASE_URL")
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_ALGORITHMS = os.environ.get('AUTH0_ALGORITHMS')
AUTH0_API_AUDIENCE = os.environ.get('AUTH0_API_AUDIENCE')