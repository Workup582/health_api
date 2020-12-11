import jinja2
from chalice import Response

from chalicelib.fam.config import templates

env = jinja2.Environment(loader=jinja2.FileSystemLoader([templates.TEMPLATES_DIR]),
                         autoescape=jinja2.select_autoescape(['html', 'xml']))


def render(template_name, context):
    if not context:
        context = {}

    context['static_url'] = templates.STATIC_URL

    template_file = f'{template_name}.html'
    return env.get_template(template_file).render(context)


def render_to_response(template_name, context, status_code=200, headers=None):
    template = render(template_name, context)

    if not headers:
        headers = {"Content-Type": "text/html", "Access-Control-Allow-Origin": "*"}

    return Response(template, status_code=status_code, headers=headers)
