import re
from urllib.parse import urlparse, parse_qs


def test_create(vidispine, cassette):
    result = vidispine.collection.create('test_collection_1')

    last_request = cassette.requests[0]
    url = urlparse(last_request.url)

    assert re.match(r'^VX-\d+$', result)
    assert cassette.play_count == 1
    assert parse_qs(url.query) == {'name': ['test_collection_1']}
