import pytest

from vidispine.client import Client, Vidispine
from vidispine.errors import NotFound


def test_vidispine_init():
    vidispine = Vidispine('http://localhost:8080', 'admin', 'admin')

    assert isinstance(vidispine.client, Client)


def test_version(cassette, vidispine):
    version_data = vidispine.version()

    assert version_data['component'][0]['name'] == 'API'
    assert cassette.play_count == 1
    assert cassette.all_played


def test_get_item_with_metadata(cassette, vidispine):
    item = vidispine.get_item('VX-12')

    assert item['id'] == 'VX-12'
    assert item['metadata']

    assert cassette.all_played


def test_get_item_without_metadata(cassette, vidispine):
    item = vidispine.get_item('VX-12', metadata=False)

    assert item['id'] == 'VX-12'
    assert item.get('metadata') is None

    assert cassette.all_played


def test_not_found_with_invalid_id(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-1000000')
