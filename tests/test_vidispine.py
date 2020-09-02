from urllib.parse import urlparse, parse_qs

import pytest
import requests_mock
import vcr

from vidispine.client import Vidispine, Client


@pytest.fixture
def vidispine():
    return Vidispine('http://localhost', 'admin', 'admin')


def test_vidispine_init():
    vidispine = Vidispine('http://localhost', 'admin', 'admin')

    assert isinstance(vidispine.client, Client)


def test_version(vidispine):
    data = {
        'component': [
            {
                'name': 'API', 'version':
                '4.12.5-g4ce4cfd-18958'
            },
            {
                'name': 'Transcoder VX-1',
                'siteId': 'VX-1',
                'version': '4.12.5-gf0c297f-18959'
            },
            {
                'name': 'Hibernate',
                'version': '4.1.9-VS-20140827'
            },
            {
                'name': 'Jersey',
                'version': '2.23.2'
            },
            {
                'name': 'Jackson', 'version': '1.9.5'
            }
        ],
        # Truncated example - no VCR to avoid sensitive license info
    }
    with requests_mock.Mocker() as m:
        m.get('http://localhost:8080/API/version', json=data)
        version_data = vidispine.version()

    assert version_data == data


class TestCreateCollection:

    def test_create(self, vidispine):
        with vcr.use_cassette(
            'tests/cassettes/create_collection.yaml'
        ) as cass:
            result = vidispine.create_collection('test_collection_1')

        last_request = cass.requests[0]
        url = urlparse(last_request.url)

        assert result == 'VX-1'
        assert cass.play_count == 1
        assert parse_qs(url.query) == {'name': ['test_collection_1']}
