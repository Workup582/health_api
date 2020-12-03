from chalice import Blueprint, Response

from chalicelib.fam import config
from chalicelib.fam.db import users
from chalicelib.fam import mapper
from chalicelib.fam import requester

query_blueprint = Blueprint(__name__)


@query_blueprint.route('/query/{path1}', methods=['POST', 'GET'])
@query_blueprint.route('/query/{path1}/{path2}', methods=['POST', 'GET'])
@query_blueprint.route('/query/{path1}/{path2}/{path3}',
                       methods=['POST', 'GET'])
def query(path1, path2=None, path3=None):
    req = query_blueprint.current_request
    path = '/'.join([p for p in (path1, path2, path3) if p])

    try:
        user = users.User.get_current_user(req)

        if not user:
            raise LookupError('User not found')

        if user.req_count <= 0:
            raise ValueError('Requests limit exceede')

        user.req_count -= 1
        user.update()
    except LookupError:
        return Response(status_code=404,
                        body={
                            'success': False,
                            'message': 'User not found'
                        })
    except ValueError:
        return Response(status_code=403,
                        body={
                            'success': False,
                            'message': 'Requests limits for account exceeded'
                        })
    except Exception as ex:
        print('Authorization failed:', ex)
        return Response(status_code=500,
                        body={
                            'success': False,
                            'message': 'Unable process request'
                        })

    res = None
    url = config.BASE_URL + mapper.translate_url(path)

    if req.method == 'POST':
        payload = req.json_body.copy()
        mapper.translate_list_with_ids(payload['evidence'])

        print(
            'Pre-POST information:', {
                'body_original': req.json_body.copy(),
                'body_translated': payload,
                'url_original': path,
                'url_translated': url
            })

        res = requester.post(url, payload)
    elif req.method == 'GET':
        query_string = mapper.translate_query_string(req.query_params)

        print(
            'Pre-GET information:', {
                'query_string_original': req.query_params,
                'query_string_translated': query_string,
                'url_original': path,
                'url_translated': url
            })

        res = requester.get(url, query_string)
    else:
        print(f'Unsupported method: {req.method}')

    try:
        json = res.json()
        mapper.intelligent_response_converter(json, 'to')
        return {'success': True, 'content': json}
    except Exception as ex:
        print(f'Unable to decode JSON from response: ${res.content}:', ex)

    return {'success': False}
