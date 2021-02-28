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
  export AWS_DEFAULT_PROFILE=<CREATED_PROFILE_NAME_OR_DEFAULT>
  ```
- Ensure that `.chalice/config.json` contains required urls and credentials for desired stage.

## Application deployment options

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

## Example deployment for PRODUCTION environment

- create DynamoDB tables: `AWS_DEFAULT_PROFILE=workup AWS_REGION=us-east-1 python ./bin/createtable.py --stage production` // already done for all envs
  - open AWS console for DynamoDB and ensure that tables create in correct region.
- deploy lambda code `chalice deploy --stage STAGE_NAME` // already done for all envs
- deploy static assets `AWS_PROFILE=YOUR_AWS_PROFILE_NAME S3_BUCKET=production-medera-ai bin/upload_assets` // already done for all envs
  - review response - it shows resulting URL and S3 bucket where it is stored.
    - open AWS console and ensure target bucket has CORS policy set:
      ```
      [
          {
              "AllowedHeaders": [],
              "AllowedMethods": [
                  "GET"
              ],
              "AllowedOrigins": [
                  "*"
              ],
              "ExposeHeaders": []
          }
      ]
      ```
- create Google Oauth credentials
  - Open Google API project you're using for credentials at `https://console.developers.google.com/apis/credentials`
  - Click "Create credentials" and choose "OAuth Client ID"
  - Pick "web app", name client meanigfully (for example "api.medera.ai-production")
  - Add "Authorized redirect URIs" (it is last option) and add there put correct redirect URL: "https://api.medera.ai/account/oauth/complete/google-oauth2"
  - Remember client ID and client secret and put it into Lambda's settings for Google.
- create LinkedIn credentials
  - Open LinkedIn developers console "https://www.linkedin.com/developers/" and create new app
  - Name it for example "medera.ai-production" and put LinkedIn company URL and click "create app"
  - Fill "authorized redirect URI" as "https://api.medera.ai/account/oauth/complete/linkedin-oauth2"
  - On "products" tab add "Sign In with LinkedIn" and await for verification finished
  - When product "signin" reviewed and approved you'll see that scopes section on "auth" tab populated with liteprofile and email scope.
  - From "auth" tab pick client ID and client secret and put it to Lambda setting
