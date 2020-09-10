import os
from typing import Dict
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError
from requests.models import Response

from vidispine.collections import Collection
from vidispine.errors import APIError, ConfigError, NotFound

PROTOCOL = 'https'


class Client:

    def __init__(
        self,
        url: str = None,
        user: str = None,
        password: str = None,
    ) -> None:
        url = self._check_config('VIDISPINE_URL', 'url', url)
        user = self._check_config('VIDISPINE_USER', 'user', user)
        pwd = self._check_config('VIDISPINE_PASSWORD', 'password', password)

        if not url.startswith('http'):
            url = f'{PROTOCOL}://{url}'

        self.base_url = urljoin(url, '/API/')
        self.auth = (user, pwd)

    def _check_config(
        self,
        env_var: str,
        name: str,
        attribute: str = None,
    ) -> str:
        if attribute:
            return attribute

        try:
            return os.environ[env_var]
        except KeyError:
            error = (
                f'{name} not provided or {env_var} '
                'set as an environmental variable'
            )
            error = f'Missing {name} or {env_var} not set'
            raise ConfigError(error)

    def _generate_headers(self) -> Dict[str, str]:
        return {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        payload: dict = None,
        params: dict = None,
    ) -> Response:
        url = urljoin(self.base_url, endpoint)

        headers = self._generate_headers()
        # Vidispine throws an error if content-type supplied with no payload
        if payload is None:
            headers.pop('content-type')

        response = requests.request(
            method, url, auth=self.auth, json=payload, headers=headers,
            params=params,
        )

        try:
            response.raise_for_status()
        except HTTPError as err:
            if response.status_code == 404:
                raise NotFound(
                    f'Endpoint not found: {method} - {url} - {response.text}'
                )
            else:
                raise APIError(
                    f'Vidispine Error: {method} - {url} - {response.text}'
                ) from err

        return response

    def request(self, method: str, endpoint: str, **kwargs: dict) -> Response:
        """Pass-through request method

        This is to be used for functionality that has not yet been
        implemented.
        """
        endpoint = endpoint.lstrip('/')
        return self._request(method, endpoint, **kwargs)

    def get(
        self,
        endpoint: str,
        params: dict = None,
    ) -> Response:
        return self._request('GET', endpoint, params=params)

    def post(
        self,
        endpoint: str,
        payload: dict = None,
        params: dict = None,
    ) -> Response:
        return self._request('POST', endpoint, payload=payload, params=params)

    def put(
        self,
        endpoint: str,
        payload: dict = None,
        params: dict = None,
    ) -> Response:
        return self._request('PUT', endpoint, payload=payload, params=params)

    def delete(
        self,
        endpoint: str,
        params: dict = None,
    ) -> Response:
        return self._request('DELETE', endpoint, params=params)


class Vidispine:

    def __init__(
        self,
        url: str = None,
        user: str = None,
        password: str = None,
    ) -> None:
        self.client = Client(url, user, password)
        self.collection = Collection(self.client)

    def version(self) -> dict:
        return self.client.get('version').json()

    def list_collections(self, metadata=True):
        if metadata:
            params = {
                'content': 'metadata'
            }
        else:
            params = {}

        endpoint = urljoin(self.client.base_url, 'collection')

        return self.client.get(endpoint, params=params).json()
