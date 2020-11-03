import time


def test_list_no_metadata(
    vidispine, cassette, create_multiple_collections
):
    test_collection_ids = create_multiple_collections(3)

    if cassette.dirty:
        # Give Vidispine enough time to create the collections.
        time.sleep(2)

    result = vidispine.collection.list()
    collections = result['collection']

    collection_ids = [c['id'] for c in collections]

    assert set(test_collection_ids).issubset(set(collection_ids))
    assert cassette.all_played


def test_list_with_metadata(
    vidispine, cassette, create_multiple_collections
):
    test_collection_ids = create_multiple_collections(3)

    if cassette.dirty:
        # Give Vidispine enough time to create the collections.
        time.sleep(2)

    result = vidispine.collection.list({'content': 'metadata'})
    collections = result['collection']

    collection_ids = [c['id'] for c in collections]

    assert set(test_collection_ids).issubset(set(collection_ids))
    assert cassette.all_played


def test_list_with_matrix_params(
    vidispine, cassette, create_multiple_collections
):
    test_collection_ids = create_multiple_collections(3)

    if cassette.dirty:
        # Give Vidispine enough time to create the collections.
        time.sleep(2)

    result = vidispine.collection.list(matrix_params={'first': 1})
    collections = result['collection']

    collection_ids = [c['id'] for c in collections]

    assert set(test_collection_ids).issubset(set(collection_ids))
    assert cassette.all_played


def test_list_with_metadata_and_matrix_params(
    vidispine, cassette, create_multiple_collections
):
    test_collection_ids = create_multiple_collections(3)

    if cassette.dirty:
        # Give Vidispine enough time to create the collections.
        time.sleep(2)

    result = vidispine.collection.list({'content': 'metadata'}, {'first': 1})
    collections = result['collection']

    collection_ids = [c['id'] for c in collections]

    assert set(test_collection_ids).issubset(set(collection_ids))
    assert cassette.all_played
