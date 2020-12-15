import os

ENV = os.getenv('ENV')
MED_SERVICE_APP_ID = os.getenv('MED_SERVICE_APP_ID')
MED_SERVICE_APP_KEY = os.getenv('MED_SERVICE_APP_KEY')
MED_SERVICE_URL = os.getenv('MED_SERVICE_URL')
BASE_URL = os.getenv('BASE_URL')

SECRET = os.getenv('APP_SECRET_KEY')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# If zero - no token expiration will set
TOKEN_EXPIRATION_SEC = 4 * 24 * 60 * 60  # 4 weeks

MAX_REQUESTS = 30
