import os

ENV = os.getenv('ENV')
APP_ID = os.getenv('c03d1c83')
APP_KEY = os.getenv('')
BASE_URL = ""

SECRET = '6c6f96239e7a4cb9bac5a6e1e933c99171e0f7975b994b9f8b0ab317fb34fadfa128aae58aa4403c8d06d334d75fb533'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REGION = os.environ['AWS_REGION']

# If zero - no token expiration will set
TOKEN_EXPIRATION_SEC = 4 * 24 * 60 * 60  # 4 weeks

MAX_REQUESTS = 30
