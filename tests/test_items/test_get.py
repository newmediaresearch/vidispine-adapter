import pytest

from vidispine.errors import NotFound


@pytest.fixture
def create_item(vidispine, cassette):
    metadata = {
        "timespan": [{
            "field": [{
                "name": "title",
                "value": [{
                    "value": "My placeholder import!"
                }]
            }],
            "start": "-INF",
            "end": "+INF"
        }]
    }

    client = vidispine.client
    endpoint = f'{client.base_url}import/placeholder'

    params = {
        'container': 1
    }

    request = client.request(
        'post',
        endpoint,
        json=metadata,
        params=params
    )

    item_id = request['id']

    return item_id


def test_get_item_with_metadata(cassette, vidispine, create_item):
    item_id = create_item

    item = vidispine.item.get(item_id)

    assert item['id'] == item_id
    assert item['metadata']
    assert cassette.all_played


def test_get_item_without_metadata(cassette, vidispine, create_item):
    item_id = create_item
    item = vidispine.item.get(item_id, metadata=False)

    assert item['id'] == item_id
    assert item.get('metadata') is None
    assert cassette.all_played


def test_not_found_with_invalid_id(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-99999999')

    err.match(
        r'Endpoint not found: GET'
    )
    assert cassette.all_played
