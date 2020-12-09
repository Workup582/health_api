import uuid
from chalice import Blueprint, Response

from chalicelib.fam.template import render_to_response
from chalicelib.fam import config
from chalicelib.fam.db import users
from chalicelib.fam.cipher import verify_password, issue_token
from chalicelib.fam.common.logger import log_call

from social_core.actions import do_auth, do_complete

from chalicelib.fam.oauth.utils import psa

account_blueprint = Blueprint(__name__)


def do_login(backend, user, social_user):
    # name = backend.strategy.setting('REMEMBER_SESSION_NAME', 'keep')
    # remember = backend.strategy.session_get(name) or \
    #            request.cookies.get(name) or \
    #            request.args.get(name) or \
    #            request.form.get(name) or \
    #            False
    # return login_user(user, remember=remember)

    user.is_authenticated = True

    if not user.social_user:
        user.social_user = social_user

    account_blueprint.current_request.user = user

    return user


@account_blueprint.route('/account/login', methods=['POST'])
def login(backend=None):
    payload = account_blueprint.current_request.json_body

    username = payload['username']
    password = payload['password']

    users_by_email = users.User.scan(email=username)

    if not users_by_email:
        return Response(status_code=404, body={'success': False, 'message': 'User not found'})

    user = users_by_email[0]

    password_matched = verify_password(user.password, password)

    if not password_matched:
        return Response(status_code=403, body={'success': False, 'message': 'Password or phone/email incorrect'})

    token = issue_token(username)

    return {'success': True, 'token': token, 'req_count': user.req_count, 'api_key': user.api_key}


@account_blueprint.route('/account/login/{backend_name}', methods=['GET'])
@psa('/account/oauth/complete/{backend_name}')
@log_call(name='OAuth login init')
def login_oauth(backend_name):
    backend = account_blueprint.current_request.backend
    return do_auth(backend)


@account_blueprint.route('/account/oauth/complete/{backend_name}', name='oauth.complete')
@psa('/account/oauth/complete/{backend_name}')
@log_call(name='OAuth login complete')
def login_oauth_complete(backend_name, *args, **kwargs):
    backend = account_blueprint.current_request.backend
    temp_anonymous_user = account_blueprint.current_request.user

    do_complete(backend, login=do_login, user=temp_anonymous_user, *args, **kwargs)

    user = account_blueprint.current_request.user

    token = issue_token(user.username)

    return render_to_response('index', {'token': token, 'api_key': user.api_key})


@account_blueprint.route('/account/register', methods=['POST'])
def register():
    payload = account_blueprint.current_request.json_body

    try:
        user = users.User(
            username=payload['username'],
            email=payload['username'],
            first_name=payload['first_name'],
            last_name=payload['last_name'],
            cleartext_password=payload['password']
        )
        user.create()
    except Exception as ex:
        print('Registration exception:', ex, payload)
        return {'success': False, 'message': 'Unable to create this account.'}

    return {'success': True}


@account_blueprint.route('/account/me', methods=['GET'])
def user_account():
    user = users.User.get_current_user(account_blueprint.current_request)

    return user.to_dict()


@account_blueprint.route('/account/me', methods=['PUT'])
def update_user():
    user = users.User.get_current_user(account_blueprint.current_request)

    if not user:
        return Response(status_code=404,
                        body={
                            'success': False,
                            'message': 'User not found'
                        })

    payload = account_blueprint.current_request.json_body.copy()

    user.first_name = payload['first_name']
    user.last_name = payload['last_name']
    user.update()

    return user.to_dict()


@account_blueprint.route('/account/me/regenerate_api_key', methods=['PUT'])
def regenerate_api_key():
    user = users.User.get_current_user(account_blueprint.current_request)

    if not user:
        return Response(status_code=404,
                        body={
                            'success': False,
                            'message': 'User not found'
                        })

    user.api_key = uuid.uuid4().hex
    user.req_count = config.MAX_REQUESTS
    user.update()

    return user.to_dict()
