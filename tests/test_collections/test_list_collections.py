import time

import pytest


@pytest.fixture
def create_multiple_collections(vidispine):
    def _create_multiple_collections(quantity):
        vidispine_ids = [
            vidispine.collection.create(f'test_collection_{i}')
            for i in range(1, quantity + 1)
        ]
        return vidispine_ids

    return _create_multiple_collections


def test_list_collections_no_metadata(
    vidispine, cassette, create_multiple_collections
):
    test_collection_ids = create_multiple_collections(3)

    # Give Vidispine enough time to create the collections.
    time.sleep(2)

    result = vidispine.list_collections()
    collections = result['collection']

    collection_ids = [c['id'] for c in collections]

    assert set(test_collection_ids).issubset(set(collection_ids))
    assert cassette.all_played


def test_list_collections_with_metadata(
    vidispine, cassette, create_multiple_collections
):
    test_collection_ids = create_multiple_collections(3)

    # Give Vidispine enough time to create the collections.
    time.sleep(2)

    result = vidispine.list_collections({'content': 'metadata'})
    collections = result['collection']
    collection_ids = set()

    for c in collections:
        fields = c['metadata']['timespan'][0]['field']
        for field in fields:
            if field['name'] == 'collectionId':
                collection_id = field['value'][0]['value']
                collection_ids.add(collection_id)
                break

    assert set(test_collection_ids).issubset(collection_ids)
    assert cassette.all_played
