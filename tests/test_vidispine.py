import re
from urllib.parse import urlparse, parse_qs

import pytest
import vcr

from vidispine.client import Vidispine, Client

my_vcr = vcr.VCR(filter_headers=['authorization'])


@pytest.fixture
def vidispine():
    return Vidispine('http://localhost', 'admin', 'admin')


def test_vidispine_init():
    vidispine = Vidispine('http://localhost', 'admin', 'admin')

    assert isinstance(vidispine.client, Client)


def test_version(vidispine):
    with my_vcr.use_cassette('tests/cassettes/version.yaml') as cass:
        version_data = vidispine.version()

    assert version_data['component'][0]['name'] == 'API'
    assert cass.play_count == 1

class TestCreateCollection:

    def test_create(self, vidispine):
        with my_vcr.use_cassette(
            'tests/cassettes/create_collection.yaml'
        ) as cass:
            result = vidispine.collection.create('test_collection_1')

        last_request = cass.requests[0]
        url = urlparse(last_request.url)

        assert re.match(r'^VX-\d+$', result)
        assert cass.play_count == 1
        assert parse_qs(url.query) == {'name': ['test_collection_1']}
