import pytest

from vidispine.errors import NotFound


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

    err.match(r'Not Found: GET')
    assert cassette.all_played
