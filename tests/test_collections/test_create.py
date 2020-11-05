import re
from urllib.parse import parse_qs, urlparse


def test_create(vidispine, cassette):
    result = vidispine.collection.create()

    last_request = cassette.requests[0]
    url = urlparse(last_request.url)

    assert re.match(r'^VX-\d+$', result)
    assert cassette.all_played
    assert url.path == '/API/collection'


def test_create_with_params(vidispine, cassette):
    result = vidispine.collection.create({'name': 'test_collection_1'})

    last_request = cassette.requests[0]
    url = urlparse(last_request.url)

    assert re.match(r'^VX-\d+$', result)
    assert cassette.all_played
    assert parse_qs(url.query) == {'name': ['test_collection_1']}
