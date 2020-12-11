STATIC_URL = 'http://localhost:8000/assets'

if config.ENV == 'staging':
    STATIC_URL = 'https://staging-medera-ai.s3.amazonaws.com'
elif config.ENV == 'production':
    STATIC_URL = 'https://production-medera-ai.s3.amazonaws.com'


TEMPLATES_DIR = 'chalicelib/templates/'
