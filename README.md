# Requirements

- Python 3.6
- Pip package manager
- (optional) Virtualenv infrastructure

# Deployment

- install virtual environment: `pip install virtualenvwrapper`
- create virtuen environment: `mkvirtualenv fam-medica`. If default Python Os version is 2.x please specify Python of
    version 3 like `mkvirtualenv -p /usr/bin/python3.6`
- activate virtualenv (if not activated automatically): `workon fam-medica`
- install app dependencies: `pip install -r requirements.txt`
- ensure that you have aws credential file `~/.aws/credentials` with content like:
    ```
    [default]
    aws_access_key_id = XXXXXXXX
    aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXX
    ```
    Corresponding ID and key can be creted in Security section on AWS Console
- create DynamoDB table for users: `python createtable.py`
- deploy application to lambda: `chalice deploy`

After deployment log information will be displayed like:
```
Creating deployment package.
Updating policy for IAM role: fam-medica-dev-api_handler
Updating lambda function: fam-medica-dev
Updating rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-1:386228871734:function:fam-medica-dev
  - Rest API URL: https://ccy9mb5095.execute-api.us-east-1.amazonaws.com/api/
```

Assume value from example log `https://ccy9mb5095.execute-api.us-east-1.amazonaws.com/api/` named below as `API_URL`.


# UI deployment

- Edit S3 bucket name for statis assets:
    - Open `/bin/upload_assets` in your favourite editor
    - Change line `BUCKET=fam-medica-assets` to `BUCKET=<YOUR_PREFERRED_BUCKET_NAME_HERE>`
- Deploy static assets: `./bin/upload_assets`
- Deploy entire code to Lambda


# REST API

- `API_URL/account/register`. Account creation endpoint. Expected payload:
    ```
    {"username": "aaa1@bbb.ccc", "password": "iddqd", "first_name": "Aaa", "last_name": "Bbb"}
    ```
    return value: `{success: true}`
- `API_URL/account/login`. Login endpoint that grant user with authorization token. Expected payload:
    ```
    {"username": "aaa1@bbb.ccc", "password": "iddqd"}
    ```
    return value (if success): { success: true, token: 'SOME STRING' }
- `API_URL/query/`. Main URL that proxifying requests to upstream provider. Here values from
    query string (for GET requests), body (for POST requests) and URL translated according to provided dictionary
    to send to upstream. Also this endpoint allows more then one URL. Accepted up to 3 additional URL parts i.e.:
    - `API_URL/query/engdiag`
    - `API_URL/query/engdiag/engtest`
    - `API_URL/query/engdiag/engtest/engresult`

    For now only `engdiag` URL part rewritten but other can be added to `mapper.py`.

    This endpoint protected and allowed only for logged on users i.e. who provides token. Token must be provided
    in `Authorization` header like: `Authorization: Bearer HERE_TOKEN_GRANTED_AFTER_LOGIN`
    One user account can send up to 30 requests, after that account will receive message `request limit exceeded`.
