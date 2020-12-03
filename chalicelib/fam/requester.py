import requests

from . import config


def prepare_headers(headers=None):
    if not headers:
        headers = {}
    else:
        headers = headers.copy()

    headers['App-Id'] = config.APP_ID
    headers['App-Key'] = config.APP_KEY

    return headers


def post(url, body, headers=None):
    headers = prepare_headers(headers)

    print(f'POST to {url} body {body} with headers {headers}')

    return requests.post(url, json=body, headers=headers)


def get(url, query_string=None, headers=None):
    headers = prepare_headers(headers)

    print(f'GET to {url} query string {query_string} with headers {headers}')

    return requests.get(url, params=query_string, headers=headers)
