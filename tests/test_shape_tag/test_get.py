import pytest

from vidispine.errors import NotFound


def test_get(vidispine, cassette, shape_tag_metadata):
    shape_tag_name = 'test'
    endpoint = f'shape-tag/{shape_tag_name}'
    vidispine.client.request('put', endpoint, json=shape_tag_metadata)

    result = vidispine.shape_tag.get(shape_tag_name)

    assert result == shape_tag_metadata

    assert cassette.all_played


def test_get_shape_tag_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.shape_tag.get('tag1000000')

    assert cassette.all_played

    err.match(r'Not Found: GET')
