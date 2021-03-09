import pytest

from vidispine.errors import InvalidInput, NotFound


@pytest.fixture
def item_with_placeholder_import(vidispine, cassette, item, sample_file):
    vidispine.item.import_to_placeholder(
        item, 'container', {'uri': sample_file}
    )
    return item


def test_transcode(vidispine, cassette, item_with_placeholder_import):
    params = {'tag': 'lowres', 'priority': 'LOWEST'}
    result = vidispine.item.transcode(item_with_placeholder_import, params)

    assert result['type'] == 'TRANSCODE'
    assert result['priority'] == 'LOWEST'
    assert cassette.all_played


def test_transcode_invalid_input(vidispine, item_with_placeholder_import):
    with pytest.raises(InvalidInput) as err:
        vidispine.item.transcode(item_with_placeholder_import, {})

    err.match('Please supply shape tags.')


def test_transcode_item_not_found(vidispine, cassette):
    params = {'tag': 'lowres'}
    with pytest.raises(NotFound) as err:
        vidispine.item.transcode('VX-1000000', params=params)

    err.match('Not Found: POST')


def test_transcode_item_without_import(vidispine, cassette, item):
    params = {'tag': 'lowres'}
    result = vidispine.item.transcode(item, params=params)

    assert result['type'] == 'TRANSCODE'
    assert cassette.all_played
