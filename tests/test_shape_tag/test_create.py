import pytest

from vidispine.errors import InvalidInput


def test_create(vidispine, cassette, shape_tag_metadata):
    shape_tag_name = 'test'
    vidispine.shape_tag.create(shape_tag_name, shape_tag_metadata)

    assert cassette.all_played


def test_create_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.shape_tag.create('test', {})

    err.match('Please supply metadata.')
