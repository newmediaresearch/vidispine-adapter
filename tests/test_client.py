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
    client = Client(base_url, 'admin', 'admin')

    assert client.base_url == expected_url
    assert client._generate_headers() == {
        'content-type': 'application/json',
        'accept': 'application/json'
    }


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
