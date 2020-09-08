from urllib.parse import urljoin

import pytest
import requests_mock

from vidispine.client import Client
from vidispine.errors import NotFound, APIError


@pytest.fixture
def test_client():
    return Client('http://localhost:8080', 'admin', 'admin')


@pytest.mark.parametrize('base_url,expected_url', [
    ('http://localhost:8080', 'http://localhost:8080/API/'),
    ('https://localhost:8080', 'https://localhost:8080/API/'),
    ('localhost', 'https://localhost/API/'),
])
def test_init(base_url, expected_url):
    user = 'admin'
    password = 'admin'
    client = Client(base_url, user, 'admin')

    assert client.base_url == expected_url
    assert client.auth == (user, password)
    assert client._generate_headers() == {
        'content-type': 'application/json',
        'accept': 'application/json'
    }


def test_init_environmental_variables(monkeypatch):
    url = 'https://example.com:8080'
    user = 'admin'
    password = 'admin'
    monkeypatch.setenv('VIDISPINE_URL', url)
    monkeypatch.setenv('VIDISPINE_USER', user)
    monkeypatch.setenv('VIDISPINE_PASSWORD', password)

    client = Client()

    expected_url = urljoin(url, '/API/')
    assert client.base_url == expected_url
    assert client.auth == (user, password)
    assert client._generate_headers() == {
        'content-type': 'application/json',
        'accept': 'application/json'
    }


def test_init_missing_url(monkeypatch):
    monkeypatch.delenv('VIDISPINE_URL', raising=False)
    with pytest.raises(ValueError):
        Client()
    try:
        Client()
    except ValueError as error:
        assert str(error) == 'url not set'


def test_init_missing_user(monkeypatch):
    monkeypatch.delenv('VIDISPINE_USER', raising=False)
    with pytest.raises(ValueError):
        Client(url='https://example.com')
    try:
        Client(url='https://example.com')
    except ValueError as error:
        assert str(error) == 'user not set'


def test_init_missing_password(monkeypatch):
    monkeypatch.delenv('VIDISPINE_PASSWORD', raising=False)
    with pytest.raises(ValueError):
        Client(url='https://example.com', user='admin')
    try:
        Client(url='https://example.com', user='admin')
    except ValueError as error:
        assert str(error) == 'password not set'


class TestRequest:
    def test_request(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.get('http://localhost:8080/API/version', json='foo')
            response = test_client._request('GET', endpoint)

        assert response.json() == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'
        assert m.last_request.headers['accept'] == 'application/json'
        assert m.last_request.headers['authorization'] == (
            'Basic YWRtaW46YWRtaW4='
        )
        assert 'content-type' not in m.last_request.headers

    def test_request_with_payload(self, test_client):
        endpoint = 'version'
        payload = {'eggs': 123}

        with requests_mock.Mocker() as m:
            m.post('http://localhost:8080/API/version', json='foo')
            response = test_client._request('POST', endpoint, payload=payload)

        assert response.json() == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'
        assert m.last_request.json() == payload
        assert m.last_request.headers['content-type'] == 'application/json'
        assert m.last_request.headers['accept'] == 'application/json'
        assert m.last_request.headers['authorization'] == (
            'Basic YWRtaW46YWRtaW4='
        )

    def test_request_with_query_params(self, test_client):
        endpoint = 'version'
        params = {'foo': 'bar'}

        with requests_mock.Mocker() as m:
            m.get('http://localhost:8080/API/version', json='foo')
            response = test_client._request('GET', endpoint, params=params)

        assert response.json() == 'foo'
        assert m.last_request.url == (
            'http://localhost:8080/API/version?foo=bar'
        )

    def test_not_found_error(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/API/version',
                status_code=404,
                text='not here',
            )

            with pytest.raises(NotFound) as err:
                test_client._request('GET', endpoint)

        assert err.value.args[0] == (
            'Endpoint not found: GET - http://localhost:8080/API/version - '
            'not here'
        )

    def test_unexpected_error(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/API/version',
                status_code=500,
                text='BOOM!!',
            )

            with pytest.raises(APIError) as err:
                test_client._request('GET', endpoint)

        assert err.value.args[0] == (
            'Vidispine Error: GET - http://localhost:8080/API/version - '
            'BOOM!!'
        )

    def test_get(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.get('http://localhost:8080/API/version', json='foo')
            response = test_client.get(endpoint)

        assert response.json() == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_delete(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.delete('http://localhost:8080/API/version', json='foo')
            response = test_client.delete(endpoint)

        assert response.json() == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_post(self, test_client):
        endpoint = 'version'
        payload = {'eggs': 123}

        with requests_mock.Mocker() as m:
            m.post('http://localhost:8080/API/version', json='foo')
            response = test_client.post(endpoint, payload)

        assert response.json() == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_put(self, test_client):
        endpoint = 'version'
        payload = {'eggs': 123}

        with requests_mock.Mocker() as m:
            m.put('http://localhost:8080/API/version', json='foo')
            response = test_client.put(endpoint, payload)

        assert response.json() == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_passthrough_request(self, test_client):
        endpoint = '/version'

        with requests_mock.Mocker() as m:
            m.get('http://localhost:8080/API/version', json='foo')
            response = test_client.request('GET', endpoint)

        assert response.json() == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'
