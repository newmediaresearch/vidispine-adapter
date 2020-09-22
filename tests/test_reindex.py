import pytest


@pytest.mark.parametrize('index', [
    'item', 'thumbnail', 'document', 'collection', 'acl'
])
def test_reindex(vidispine, cassette, index):
    index = 'thumbnail'
    result = vidispine.reindex(index)

    assert result['index'] == index
    assert cassette.all_played
