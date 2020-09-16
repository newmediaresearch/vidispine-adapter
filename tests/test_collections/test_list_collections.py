import time

import pytest


@pytest.fixture
def delete_all_collections(vidispine):
    def _delete_all_collections():
        result = vidispine.list_collections()
        collections = result['collection']

        for collection in collections:
            vidispine.collection.delete(collection['id'])

    return _delete_all_collections


def test_list_collections_not_found(
    vidispine, cassette, delete_all_collections
):
    delete_all_collections()
    result = vidispine.list_collections()

    assert result['hits'] == 0
    assert cassette.all_played


def test_list_collections_no_metadata(vidispine, cassette):
    test_collections = [
        'test_collection_1',
        'test_collection_2',
        'test_collection_3'
    ]

    for collection in test_collections:
        vidispine.collection.create(collection)

    # Give Vidispine enough time to create the collections.
    time.sleep(2)

    result = vidispine.list_collections()
    collections = result['collection']

    test_collections.reverse()

    for index, collection in enumerate(test_collections):
        assert collections[index]['name'] == collection

    assert cassette.all_played


def test_list_collections_with_metadata(
    vidispine, cassette, check_field_value_exists
):
    test_collections = [
        'test_collection_1',
        'test_collection_2',
        'test_collection_3'
    ]

    for collection in test_collections:
        vidispine.collection.create(collection)

    # Give Vidispine enough time to create the collections.
    time.sleep(2)

    result = vidispine.list_collections(['metadata'])
    collections = result['collection']

    test_collections.reverse()

    for index, collection in enumerate(test_collections):
        fields = collections[index]['metadata']['timespan'][0]['field']
        check_field_value_exists(fields, 'title', collection)

    assert cassette.all_played
