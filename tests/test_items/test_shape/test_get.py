import pytest

from vidispine.errors import NotFound


def test_get_without_params(vidispine, cassette, item, create_shape):
    shape_id = create_shape(item)

    result = vidispine.item_shape.get(item, shape_id)

    assert result['uri']['id'] == shape_id
    assert cassette.all_played


def test_get_with_params(vidispine, cassette, item, create_shape):
    shape_id = create_shape(item)

    result = vidispine.item_shape.get(
        item, shape_id, {'transient': True, 'includePlaceholder': True}
    )

    assert result['uri']['id'] == shape_id
    assert cassette.all_played


def test_get_item_not_found(vidispine, cassette):
    item_id = 'VX-1000000'

    with pytest.raises(NotFound) as err:
        vidispine.item_shape.get(item_id, 'VX-1')

    err.match('Not Found: GET')
    assert cassette.all_played


def test_get_shape_not_found(vidispine, cassette, item):
    shape_id = 'VX-1000000'

    with pytest.raises(NotFound) as err:
        vidispine.item_shape.get(item, shape_id)

    err.match('Not Found: GET')
    assert cassette.all_played
