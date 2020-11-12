import pytest
import re
from vidispine.errors import InvalidInput, NotFound


@pytest.fixture
def metadata():
    return {'id': 'VX'}


def test_create(vidispine, cassette, metadata, item):
    result = vidispine.item_shape.create(metadata, item)

    assert re.match(r'^VX-\d+$', result['id'])
    assert cassette.all_played


def test_create_with_metadata(vidispine, cassette, metadata, item):
    result = vidispine.item_shape.create(
        metadata, item, {'updateItemMetadata': True}
    )

    assert re.match(r'^VX-\d+$', result['id'])
    assert cassette.all_played


def test_create_item_not_found(vidispine, cassette, metadata):
    item_id = 'VX-1000000'

    with pytest.raises(NotFound) as err:
        vidispine.item_shape.create(metadata, item_id)

    err.match('Not Found: POST')
    assert cassette.all_played


def test_create_invalid_input(vidispine, item):
    with pytest.raises(InvalidInput) as err:
        vidispine.item_shape.create({}, item)

    err.match('Please supply metadata.')
