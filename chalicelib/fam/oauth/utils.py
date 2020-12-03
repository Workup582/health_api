from functools import wraps
from chalice import BadRequestError

from social_core.backends.utils import load_backends
from social_core.backends.linkedin import LinkedinOAuth2
from social_core.backends.google import GoogleOAuth2

from chalicelib.fam.oauth.strategy import ChaliceStrategy
from chalicelib.fam.oauth.storage import DynamoDBStorage
from chalicelib.fam.config import oauth

from chalicelib.fam.application import app

BACKENDS = {'linkedin-oauth2': LinkedinOAuth2, 'google-oauth2': GoogleOAuth2}


def psa(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(backend_name, *args, **kwargs):
            load_backends(oauth.SOCIAL_AUTH_AUTHENTICATION_BACKENDS)

            storage = DynamoDBStorage()
            strategy = ChaliceStrategy(storage=storage)
            Backend = BACKENDS.get(backend_name)

            if not Backend:
                raise BadRequestError(f'Unable to login user via {backend_name}')

            uri = redirect_uri.replace('{backend_name}', backend_name)

            app.current_request.strategy = strategy
            app.current_request.backend = Backend(strategy=strategy, redirect_uri=uri)
            return func(backend_name, *args, **kwargs)

        return wrapper

    return decorator
