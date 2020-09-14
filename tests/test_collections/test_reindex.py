def test_reindex_collection(vidispine, cassette):
    index = 'collection'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played


def test_reindex_item(vidispine, cassette):
    index = 'item'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played


def test_reindex_index_not_found(vidispine, cassette):
    index = 'foo'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played
