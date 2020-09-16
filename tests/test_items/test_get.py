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
        payload=metadata,
        params=params
    )

    item_id = request.json()['id']

    return item_id


def test_get_item_with_metadata(cassette, vidispine, create_item):
    item_id = create_item

    item = vidispine.item.get(item_id)

    assert item['id'] == item_id
    assert item['metadata']


def test_get_item_without_metadata(cassette, vidispine, create_item):
    item_id = create_item
    item = vidispine.item.get(item_id, metadata=False)

    assert item['id'] == item_id
    assert item.get('metadata') is None


def test_not_found_with_invalid_id(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-12')

    err.match(
        r'Endpoint not found: GET'
    )
