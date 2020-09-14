import pytest


@pytest.fixture
def create_multiple_collections(vidispine):
    def _create_multiple_collections(quantity):
        vidispine_ids = [vidispine.collection.create(
            f'test_collection_{i + 1}'
        )
            for i in range(quantity)
        ]

        return vidispine_ids

    return _create_multiple_collections


def test_delete_multiple(vidispine, cassette, create_multiple_collections):
    vidispine_ids = create_multiple_collections(3)

    vidispine.collection.delete_multiple(vidispine_ids)

    assert cassette.all_played


def test_delete_multiple_not_found(vidispine, cassette, create_collection):
    collection_2 = 'VX-1000000'

    vidispine.collection.delete_multiple([create_collection, collection_2])

    assert cassette.all_played
