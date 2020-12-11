from . import ENV

STATIC_URL = 'http://localhost:8000/assets'

if ENV == 'staging':
    STATIC_URL = 'https://staging-medera-ai.s3.amazonaws.com'
elif ENV == 'production':
    STATIC_URL = 'https://production-medera-ai.s3.amazonaws.com'


TEMPLATES_DIR = 'chalicelib/templates/'
