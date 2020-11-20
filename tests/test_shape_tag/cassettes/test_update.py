import json
from urllib.parse import urlparse

import pytest

from vidispine.errors import InvalidInput


def test_update(vidispine, cassette, shape_tag_metadata):
    shape_tag_name = 'test'

    vidispine.client.request(
        'put', f'shape-tag/{shape_tag_name}', json=shape_tag_metadata
    )

    vidispine.shape_tag.update(shape_tag_name, {"format": "mxf"})

    request = cassette.requests[0]

    assert request.method == 'PUT'
    assert json.loads(request.body) == shape_tag_metadata
    assert urlparse(request.url).path == f'/API/shape-tag/{shape_tag_name}'

    assert cassette.all_played


def test_update_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.shape_tag.update('test', {})

    err.match('Please supply metadata.')
