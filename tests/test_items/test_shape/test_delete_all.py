import pytest

from vidispine.errors import NotFound


def test_delete_all(vidispine, cassette, item, create_multiple_shapes):
    create_multiple_shapes(item, 3)
    vidispine.item_shape.delete_all(item)

    assert cassette.all_played


def test_delete_all_with_params(
    vidispine, cassette, item, create_multiple_shapes
):
    create_multiple_shapes(item, 3)
    vidispine.item_shape.delete_all(item, {'keepFiles': True})

    assert cassette.all_played


def test_delete_all_item_not_found(vidispine, cassette):
    item_id = 'VX-1000000'

    with pytest.raises(NotFound) as err:
        vidispine.item_shape.list(item_id)

    err.match('Not Found: GET')
    assert cassette.all_played
