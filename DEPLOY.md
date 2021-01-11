# Application deployment

## Prerequisites

To develop and deploy application following tools reqired:

- Python 3.8
- AWS account with administrative permissions. Following credentials and settings must be known/defined:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
- `virtualenv` or (preferably) `virtualenvwrapper` installed globally or per-user
    ```
    pip install --user virtualenvwrapper
    ```
    - All instructions blow aimed to be used with `virtualenvwrapper`
- AWS CLI installed globally or per-user
    ```
    pip install awscli
    ```
    - Define AWS credentials via `aws configure` call
- OAuth credentials created:
    - Google, create credentials under OAuth console for Web login. Also must be specified redirect URL to that login
        process redirect user on successful login
        - `GOOGLE_OAUTH2_KEY`
        - `GOOGLE_OAUTH2_SECRET`
        - `GOOGLE_REDIRECT_URL`
    - LonkedIn, create application with key and secret. Also specifu redirect URL
        - `LINKEDIN_OAUTH2_KEY`
        - `LINKEDIN_OAUTH2_SECRET`
        - `LINKEDIN_REDIRECT_URL`


## Install required dependencies

- Create virtual environment (will be activated automatically):
    ```
    mkvirtualenv workup
    ```
    - If OS contains multiple Python installation and version 3.8 isn't default it is strongly recommended to specify
        version explicitly:
        ```
        mkvirtualenv -p /usr/bin/python3.8 workup
        ```
- Install packages
    ```
    pip instal -r requirements.txt
    ```
- Define environment variable to specify AWS profile (if it isn't 'default')
    ```
    export AWS_PROFILE=<CREATED_PROFILE_NAME_OR_DEFAULT>
    ```
- Ensure that `.chalice/config.json` contains required urls and credentials for desired stage.

## Deploy application

Application supports 3 stages to deploy:
  - `dev`
  - `staging`
  - `production`

Full list if stages can be found in `.chalice/config.json` alongside with corresponding environment variables.

Deployment performed via call:
```
chalice deploy --stage <STAGE_TO_DEPLOY>
```

Once deployment finished app url will be shown, so it is time to define post-login redirect URL for OAuth apps
if it wasn't done before.
