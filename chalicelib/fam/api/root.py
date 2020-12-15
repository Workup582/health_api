import os
import mimetypes
from chalice import Blueprint, Response
from chalicelib.fam.template import render_to_response
from chalicelib.fam.db import users, social_auth, errors
import json
from chalicelib.fam import config
from chalicelib.fam.config import oauth

root_blueprint = Blueprint(__name__)


@root_blueprint.route('/')
def index():
    return render_to_response('index', {  })


@root_blueprint.route('/x/test-ddb')
def test_ddb():
    return {
        'users table': users.table.name if users.table else None,
        'social auth table': social_auth.table.name if social_auth.table else None,
        'errors table': errors.table.name if errors.table else None
    }

@root_blueprint.route('/x/test-ddb-get')
def test_ddb_get():
    qs = root_blueprint.current_request.query_params

    username = qs.get('username') if qs else None

    if username:
        auths = social_auth.SocialAuth.scan(username=username)

        return [auth.to_dict(create=True) for auth in auths]

    return 'No username'


@root_blueprint.route('/x/test-cfg')
def test_cfg():
    return {
        'config': {
            'ENV': config.ENV,
            'MED_SERVICE_APP_ID': config.MED_SERVICE_APP_ID,
            'MED_SERVICE_APP_KEY': config.MED_SERVICE_APP_KEY,
            'BASE_URL': config.BASE_URL,
            'SECRET': config.SECRET,
            'AWS_ACCESS_KEY_ID': config.AWS_ACCESS_KEY_ID,
            'AWS_SECRET_ACCESS_KEY': config.AWS_SECRET_ACCESS_KEY,
            'AWS_REGION': config.AWS_REGION,
            'TOKEN_EXPIRATION_SEC': config.TOKEN_EXPIRATION_SEC,
            'MAX_REQUESTS': config.MAX_REQUESTS,
        },
        'oauth': {
            'SOCIAL_AUTH_LOGIN_REDIRECT_URL': oauth.SOCIAL_AUTH_LOGIN_REDIRECT_URL,
            'SOCIAL_AUTH_LOGIN_ERROR_URL': oauth.SOCIAL_AUTH_LOGIN_ERROR_URL,
            'SOCIAL_AUTH_LOGIN_URL': oauth.SOCIAL_AUTH_LOGIN_URL,
            'SOCIAL_AUTH_NEW_USER_REDIRECT_URL': oauth.SOCIAL_AUTH_NEW_USER_REDIRECT_URL,
            'SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL': oauth.SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL,
            'SOCIAL_AUTH_DISCONNECT_REDIRECT_URL': oauth.SOCIAL_AUTH_DISCONNECT_REDIRECT_URL,
            'SOCIAL_AUTH_INACTIVE_USER_URL': oauth.SOCIAL_AUTH_INACTIVE_USER_URL,
            'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': oauth.SOCIAL_AUTH_AUTHENTICATION_BACKENDS,
            'SOCIAL_AUTH_PIPELINE': oauth.SOCIAL_AUTH_PIPELINE,
            'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY': oauth.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET': oauth.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY': oauth.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
            'SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET': oauth.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET,
            'SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA': oauth.SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA,
            'SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE': oauth.SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE,
            'SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS': oauth.SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS,
        }
    }

# Do not use on prod!
@root_blueprint.route('/assets/{directory}/{filename}', methods=['GET'])
def assets(directory, filename):
    headers = {'Content-Type': 'text/plain'}

    try:
        with open(f'./assets/{directory}/{filename}', 'rb') as f:
            (name, ext) = os.path.splitext(filename)

            try:
                headers['Content-Type'], _ = mimetypes.guess_type(filename)
            except Exception:
                pass

            content = f.read()

            return Response(body=content, headers=headers)
    except Exception:
        return Response(body='', headers=headers)
