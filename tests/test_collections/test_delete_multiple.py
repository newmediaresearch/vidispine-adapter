import pytest

from vidispine.errors import InvalidInput


@pytest.fixture
def create_multiple_collections(vidispine):
    def _create_multiple_collections(quantity):
        vidispine_ids = [
            vidispine.collection.create(f'test_collection_{i}')
            for i in range(1, quantity + 1)
        ]

        return vidispine_ids

    return _create_multiple_collections


def test_delete_multiple(vidispine, cassette, create_multiple_collections):
    vidispine_ids = create_multiple_collections(3)

    vidispine.collection.delete_multiple(vidispine_ids)

    assert cassette.all_played


def test_delete_multiple_not_found(vidispine, cassette, collection):
    collection_2 = 'VX-1000000'

    vidispine.collection.delete_multiple([collection, collection_2])

    assert cassette.all_played


def test_delete_multiple_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.collection.delete_multiple([])

    err.match('Please supply Vidispine IDs to delete.')
