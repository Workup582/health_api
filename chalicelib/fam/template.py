import jinja2
from chalice import Response

from chalicelib.fam import config

STATIC_URL = 'http://localhost:8000/assets' if config.ENV == 'development' else 'https://fam-medica-assets-2.s3.amazonaws.com'
TEMPLATES_DIR = 'chalicelib/templates/'

env = jinja2.Environment(loader=jinja2.FileSystemLoader([TEMPLATES_DIR]),
                         autoescape=jinja2.select_autoescape(['html', 'xml']))


def render(template_name, context):
    if not context:
        context = {}

    context['static_url'] = STATIC_URL

    template_file = f'{template_name}.html'
    return env.get_template(template_file).render(context)


def render_to_response(template_name, context, status_code=200, headers=None):
    template = render(template_name, context)

    if not headers:
        headers = {"Content-Type": "text/html", "Access-Control-Allow-Origin": "*"}

    return Response(template, status_code=status_code, headers=headers)
