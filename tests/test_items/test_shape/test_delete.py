import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, item, create_shape):
    shape_id = create_shape(item)
    vidispine.item_shape.delete(item, shape_id)

    assert cassette.all_played


def test_delete_with_params(vidispine, cassette, item, create_shape):
    shape_id = create_shape(item)
    vidispine.item_shape.delete(item, shape_id, {'updateMetadata': True})

    assert cassette.all_played


def test_delete_non_existent_item(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.item_shape.delete('VX-1000000', 'VX-1')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')


def test_delete_non_existent_shape(vidispine, cassette, item):
    with pytest.raises(NotFound) as err:
        vidispine.item_shape.delete(item, 'VX-1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
