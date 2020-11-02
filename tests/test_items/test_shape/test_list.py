import pytest

from vidispine.errors import NotFound


def test_list(vidispine, cassette, item, create_shape):
    shape_id = create_shape(item)

    result = vidispine.item_shape.list(item)

    assert shape_id in result['uri']
    assert cassette.all_played


def test_list_item_not_found(vidispine, cassette):
    item_id = 'VX-1000000'

    with pytest.raises(NotFound) as err:
        vidispine.item_shape.list(item_id)

    err.match('Not Found: GET')
    assert cassette.all_played
