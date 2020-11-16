import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, shape_tag_metadata):
    shape_tag_name = 'test'
    endpoint = f'shape-tag/{shape_tag_name}'
    vidispine.client.request('put', endpoint, json=shape_tag_metadata)

    vidispine.shape_tag.delete(shape_tag_name)

    assert cassette.all_played


def test_delete_shape_tag_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.shape_tag.delete('tag1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
