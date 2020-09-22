def test_reindex_acl(vidispine, cassette):
    index = 'acl'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played


def test_reindex_collection(vidispine, cassette):
    index = 'collection'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played


def test_reindex_document(vidispine, cassette):
    index = 'document'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played


def test_reindex_item(vidispine, cassette):
    index = 'item'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played


def test_reindex_thumbnail(vidispine, cassette):
    index = 'thumbnail'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played
