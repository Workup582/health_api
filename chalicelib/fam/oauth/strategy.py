from chalice import Response
from social_core.strategy import BaseStrategy, BaseTemplateStrategy

from chalicelib.fam.application import app
from chalicelib.fam.config import oauth
from chalicelib.fam.common.utils import build_absolute_uri, get_base_url
# from chalicelib.fam.common.logger import log_call


class ChaliceApiTemplateStrategy(BaseTemplateStrategy):
    pass


class Cookie:
    def __init__(self):
        self.name = None
        self.value = None
        self.max_age = None
        self.expires = None
        self.path = None
        self.path = '/'
        self.http_only = True

    # @log_call(name='Cookie')
    def set(self, name, value, max_age=None, path=None, http_only=True):
        self.name = name
        self.value = value
        self.max_age = max_age
        self.path = path
        self.http_only = http_only

    # @log_call(name='Cookie')
    def get(self, req, name, header='Cookie', default=None):
        cookies = req.headers.get(header) or req.headers.get('cookie')

        if cookies:
            for cookie in cookies.split(' '):
                key, value = cookie.split('=')

                if key == name:
                    return value or default

        return default

    # @log_call(name='Cookie')
    def remove(self, name):
        self.name = name
        self.value = 'REMOVED'
        self.expires = 'Thu, 01 Jan 1970 00:00:00 GMT'

    # @log_call(name='Cookie')
    def serialize(self):
        if not self.name or not self.value:
            return ''

        a = []
        a.append(f'{self.name}={self.value}')

        if self.max_age:
            a.append(f'max-age={self.max_age}')

        if self.expires:
            a.append(f'expires={self.expires}')

        if self.path:
            a.append(f'path={self.path}')

        if self.http_only:
            a.append('httpOnly')

        return '; '.join(a)

    # @log_call(name='Cookie')
    def reset(self):
        self.name = None
        self.value = None
        self.max_age = None
        self.path = '/'
        self.path = None
        self.http_only = True


class ChaliceStrategy(BaseStrategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.req = app.current_request
        self.cookie = Cookie()

    # @log_call(name='ChaliceStrategy')
    def request_data(self, merge=False):
        data = self.req.json_body.copy() if self.req.json_body else {}
        data.update(self.req.query_params or {})

        return data

    # @log_call(name='ChaliceStrategy')
    def request_host(self):
        return get_base_url(self.req)

    # @log_call(name='ChaliceStrategy')
    def build_absolute_uri(self, path=None):
        uri = build_absolute_uri(self.req, path)
        return uri

    # @log_call(name='ChaliceStrategy')
    def get_setting(self, name):
        setting = getattr(oauth, name, None)

        if setting is None:
            raise KeyError(name)

        return setting

    # @log_call(name='ChaliceStrategy')
    def redirect(self, url):
        headers = {'Location': url}

        if self.cookie.serialize():
            headers['Set-Cookie'] = self.cookie.serialize()

        return Response(status_code=302, body='', headers=headers)

    # @log_call(name='ChaliceStrategy')
    def session_get(self, name, default=None):
        value = self.cookie.get(self.req, name, default=default)

        return value

    # @log_call(name='ChaliceStrategy')
    def session_set(self, name, value):
        self.cookie.set(name, value, max_age=60, http_only=True, path='/')

    # @log_call(name='ChaliceStrategy')
    def session_pop(self, name):
        value = self.cookie.get(self.req, name)
        self.cookie.remove(self.cookie.name)
        return value

    # @log_call(name='ChaliceStrategy')
    def request_is_secure(self):
        return True

    # @log_call(name='ChaliceStrategy')
    def request_path(self):
        return self.req.path
