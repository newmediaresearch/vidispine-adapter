from urllib.parse import urljoin

import pytest
import requests_mock

from vidispine.client import Client
from vidispine.errors import APIError, ConfigError, NotFound


@pytest.fixture
def test_client() -> Client:
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
    with pytest.raises(ConfigError) as error:
        Client()
    error.match('Missing url or VIDISPINE_URL not set')


def test_init_missing_user(monkeypatch):
    monkeypatch.delenv('VIDISPINE_USER', raising=False)
    with pytest.raises(ConfigError) as error:
        Client(url='https://example.com')
    error.match('Missing user or VIDISPINE_USER not set')


def test_init_missing_password(monkeypatch):
    monkeypatch.delenv('VIDISPINE_PASSWORD', raising=False)
    with pytest.raises(ConfigError) as error:
        Client(url='https://example.com', user='admin')
    error.match('Missing password or VIDISPINE_PASSWORD not set')


class TestRequest:
    def test_request(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client._request('GET', endpoint)

        assert response == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'
        assert m.last_request.headers['accept'] == 'application/json'
        assert m.last_request.headers['authorization'] == (
            'Basic YWRtaW46YWRtaW4='
        )
        assert 'content-type' not in m.last_request.headers

    def test_request_with_json(self, test_client):
        endpoint = 'version'
        json = {'eggs': 123}

        with requests_mock.Mocker() as m:
            m.post(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client._request('POST', endpoint, json=json)

        assert response == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'
        assert m.last_request.json() == json
        assert m.last_request.headers['content-type'] == 'application/json'
        assert m.last_request.headers['accept'] == 'application/json'
        assert m.last_request.headers['authorization'] == (
            'Basic YWRtaW46YWRtaW4='
        )

    def test_request_with_data(self, test_client):
        endpoint = 'version'
        data = '<xml />'

        with requests_mock.Mocker() as m:
            m.post(
                'http://localhost:8080/API/version',
                text=data,
                headers={'Content-Type': 'application/xml'}
            )
            response = test_client._request('POST', endpoint, data=data)

        assert response == data
        assert m.last_request.url == 'http://localhost:8080/API/version'
        assert m.last_request.text == data
        assert m.last_request.headers['content-type'] == 'application/json'
        assert m.last_request.headers['accept'] == 'application/json'
        assert m.last_request.headers['authorization'] == (
            'Basic YWRtaW46YWRtaW4='
        )

    def test_request_with_query_params(self, test_client):
        endpoint = 'version'
        params = {'foo': 'bar'}

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client._request('GET', endpoint, params=params)

        assert response == 'foo'
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
            m.get(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client.get(endpoint)

        assert response == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_delete(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.delete(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client.delete(endpoint)

        assert response == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_post(self, test_client):
        endpoint = 'version'
        json = {'eggs': 123}

        with requests_mock.Mocker() as m:
            m.post(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client.post(endpoint, json=json)

        assert response == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_put(self, test_client):
        endpoint = 'version'
        json = {'eggs': 123}

        with requests_mock.Mocker() as m:
            m.put(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client.put(endpoint, json=json)

        assert response == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_passthrough_request(self, test_client):
        endpoint = 'version'

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/API/version',
                json='foo',
                headers={'Content-Type': 'application/json'}
            )
            response = test_client.request('GET', endpoint)

        assert response == 'foo'
        assert m.last_request.url == 'http://localhost:8080/API/version'

    def test_headers(self, test_client):
        endpoint = 'version'
        accept = 'text/plain'
        with requests_mock.Mocker() as m:
            headers = {'accept': accept}
            m.get('http://localhost:8080/API/version')
            test_client.get(endpoint, headers=headers)

        assert m.last_request.headers['accept'] == accept

    def test_runas(self, test_client):
        endpoint = 'version'
        runas = 'admin'
        with requests_mock.Mocker() as m:
            m.get('http://localhost:8080/API/version')
            test_client.get(endpoint, runas=runas)

        assert m.last_request.headers['runas'] == runas

    def test_runas_in_header(self, test_client):
        endpoint = 'version'
        runas = 'admin'
        with requests_mock.Mocker() as m:
            headers = {'runas': runas}
            m.get('http://localhost:8080/API/version')
            test_client.get(endpoint, headers=headers, runas='notused')

        assert m.last_request.headers['runas'] == runas

    def test_no_content(self, test_client):
        endpoint = 'version'
        with requests_mock.Mocker() as m:
            m.get('http://localhost:8080/API/version', status_code=204)
            response = test_client.get(endpoint)

        assert response == ''
