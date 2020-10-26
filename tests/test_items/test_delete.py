import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, item):
    vidispine.item.delete(item)

    with pytest.raises(NotFound):
        vidispine.item.get(item)

    assert cassette.all_played


def test_delete_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.item.delete('VX-1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
