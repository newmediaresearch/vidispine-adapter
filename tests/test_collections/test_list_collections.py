
def test_list_collections_no_metadata(vidispine, cassette):
    vidispine.collection.create('test_collection_1')

    result = vidispine.list_collections(metadata=False)
    collections = result['collection']

    assert collections[0]['name'] == 'test_collection_1'
    assert cassette.all_played


def test_list_collections_with_metadata(
    vidispine, cassette, check_field_value_exists
):
    vidispine.collection.create('test_collection_1')

    result = vidispine.list_collections()
    collections = result['collection']
    fields = collections[0]['metadata']['timespan'][0]['field']

    check_field_value_exists(fields, 'title', 'test_collection_1')
    assert cassette.all_played
