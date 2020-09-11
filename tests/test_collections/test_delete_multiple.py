def test_delete_multiple(vidispine, cassette, create_collection):
    collection_2 = vidispine.collection.create('test_collection_2')

    vidispine.collection.delete_multiple([create_collection, collection_2])

    assert cassette.all_played


def test_delete_multiple_not_found(vidispine, cassette, create_collection):
    collection_2 = 'VX-1000000'

    vidispine.collection.delete_multiple([create_collection, collection_2])

    assert cassette.all_played
