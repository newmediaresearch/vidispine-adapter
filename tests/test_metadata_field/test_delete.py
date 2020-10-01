import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, metadata_field):
    vidispine.metadata_field.delete(metadata_field)

    assert cassette.all_played


def test_delete_field_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field.delete('field1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
