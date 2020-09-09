import re
from urllib.parse import parse_qs, urlparse


def test_create(vidispine, cassette):
    result = vidispine.collection.create('test_collection_1')

    last_request = cassette.requests[0]
    url = urlparse(last_request.url)

    assert re.match(r'^VX-\d+$', result)
    assert cassette.all_played
    assert parse_qs(url.query) == {'name': ['test_collection_1']}
