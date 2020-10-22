import pytest

from vidispine.errors import NotFound


@pytest.fixture
def create_shape(vidispine, cassette):
    def _create_shape(item_id):
        metadata = {
            'id': 'new_shape'
        }

        endpoint = f'item/{item_id}/shape/create'

        result = vidispine.client.request('post', endpoint, json=metadata)

        return result['id']

    return _create_shape


def test_list(vidispine, cassette, create_item, create_shape):
    shape_id = create_shape(create_item)

    result = vidispine.item_shape.list(create_item)

    assert shape_id in result['uri']
    assert cassette.all_played


def test_list_item_not_found(vidispine, cassette):
    item_id = 'VX-1000000'

    with pytest.raises(NotFound) as err:
        vidispine.item_shape.list(item_id)

    err.match('Not Found: GET')
    assert cassette.all_played
