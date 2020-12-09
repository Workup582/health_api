from chalice import Chalice
from chalicelib.fam.common.aws import get_session
from chalicelib.fam.db import users

get_session()

app = Chalice(app_name='fam-medica')


@app.middleware('all')
def my_middleware(event, get_response):
    app.current_request.user = users.AnonymousUser

    response = get_response(event)
    return response
