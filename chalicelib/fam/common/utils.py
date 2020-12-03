def build_absolute_uri(req, path=None):
    schema = req.headers.get('x-forwarded-proto', 'http')
    host = req.headers['host']
    path = req.context['path'] if not path else path
    return f'{schema}://{host}{path}'


def get_base_url(req):
    schema = req.headers.get('x-forwarded-proto', 'http')
    host = req.headers['host']
    return f'{schema}://{host}'
