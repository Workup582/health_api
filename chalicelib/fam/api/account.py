import time
import jwt
from chalice import Blueprint, Response

from chalicelib.fam import config
from chalicelib.fam.db import users
from chalicelib.fam.cipher import verify_password
from chalicelib.fam.common.logger import log_call

from social_core.actions import do_auth, do_complete, do_disconnect

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
    print('>> do_login backend', backend)
    print('>> do_login user', user)
    print('>> do_login social_user', social_user)


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

    if config.TOKEN_EXPIRATION_SEC:
        expired_at = int(time.time()) + config.TOKEN_EXPIRATION_SEC
        token = jwt.encode({'username': username, 'exp': expired_at}, config.SECRET, algorithm='HS256').decode('ascii')
    else:
        token = jwt.encode({'username': username}, config.SECRET, algorithm='HS256').decode('ascii')

    return {'success': True, 'token': token, 'req_count': user.req_count}


@account_blueprint.route('/account/login/{backend_name}', methods=['GET'])
@psa('/account/oauth/complete/{backend_name}')
@log_call(name='OAuth login init')
def login_oauth(backend_name):
    backend = account_blueprint.current_request.backend
    return do_auth(backend, 'http://127.0.0.1:5000/account/oaut-complete')


@account_blueprint.route('/account/oauth/complete/{backend_name}', name='oauth.complete')
@psa('/account/oauth/complete/{backend_name}')
@log_call(name='OAuth login complete')
def login_oauth_complete(backend_name, *args, **kwargs):
    backend = account_blueprint.current_request.backend
    user = account_blueprint.current_request.user
    result = do_complete(backend, login=do_login, user=user, *args, **kwargs)

    print('>>>> do_complete result:', result)


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
    return users.User.get_current_user(account_blueprint.current_request)
