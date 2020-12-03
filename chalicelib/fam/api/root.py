import os
import mimetypes
from chalice import Blueprint, Response
from chalicelib.fam.template import render_to_response
from chalicelib.fam.db import users, errors

root_blueprint = Blueprint(__name__)


@root_blueprint.route('/')
def index():
    return render_to_response('index', {})


@root_blueprint.route('/test-ddb')
def test_ddb():
    return {
        'users table': users.table.name if users.table else None,
        'errors table': errors.table.name if errors.table else None
    }


# Do not use on prod!
@root_blueprint.route('/assets/{directory}/{filename}', methods=['GET'])
def assets(directory, filename):
    # print('--- Request info start ---')
    # req = root_blueprint.current_request
    # print('--- req.context: ', req.context)
    # print('--- req.headers: ', req.headers)
    # print('--- req.json_body: ', req.json_body)
    # print('--- req.lambda_context: ', req.lambda_context)
    # print('--- req.method: ', req.method)
    # print('--- req.path: ', req.path)
    # print('--- req.query_params: ', req.query_params)
    # print('--- req.uri_params: ', req.uri_params)
    # print('--- req.to_dict(): ', req.to_dict())
    # print('--- Request info end ---')

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
