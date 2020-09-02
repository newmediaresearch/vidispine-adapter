from base64 import b64encode
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError

from vidispine.errors import NotFound, VidispineAPIError

HTTP = 'http'


class Client:

    def __init__(self, url, user, password, port=8080):
        if not url.startswith('http'):
            url = f'{HTTP}://{url}'

        self.base_url = f'{url}:{port}/API/'
        self.auth = _get_basic_auth(user, password)

    def _generate_headers(self):
        return {
            'authorization': f'Basic {self.auth}',
            'content-type': 'application/json',
            'accept': 'application/json'
        }

    def _request(self, method, endpoint, payload=None, query_params=None):
        url = urljoin(self.base_url, endpoint)

        headers = self._generate_headers()
        # Vidispine throws an error if content-type supplied with no payload
        if payload is None:
            headers.pop('content-type')

        response = requests.request(
            method, url, json=payload, headers=headers, params=query_params,
        )

        try:
            response.raise_for_status()
        except HTTPError as err:
            if response.status_code == 404:
                raise NotFound(
                    f'Endpoint not found: {method} - {url} - {response.text}'
                )
            else:
                raise VidispineAPIError(
                    f'Vidispine Error: {method} - {url} - {response.text}'
                ) from err

        return response.json()

    def get(self, endpoint, query_params=None):
        return self._request('GET', endpoint, query_params=query_params)

    def post(self, endpoint, payload=None, query_params=None):
        return self._request(
            'POST', endpoint, payload=payload, query_params=query_params
        )

    def put(self, endpoint, payload=None, query_params=None):
        return self._request(
            'PUT', endpoint, payload=payload, query_params=query_params
        )

    def delete(self, endpoint, query_params=None):
        return self._request('DELETE', endpoint, query_params=query_params)


class Vidispine:

    def __init__(self, url, user, password, port=8080):
        self.client = Client(url, user, password, port=8080)

    def version(self):
        return self.client.get('version')

    def create_collection(self, name):
        query_params = {'name': name}

        response = self.client.post('collection', query_params=query_params)

        return response['id']


def _get_basic_auth(user, password):
    auth = b64encode(f'{user}:{password}'.encode())
    return auth.decode()
