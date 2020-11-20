import pytest


@pytest.fixture
def shape_tags(vidispine, cassette, shape_tag_metadata):
    shape_tag_names = ['test1', 'test2', 'test3']

    for shape_tag in shape_tag_names:
        endpoint = f'shape-tag/{shape_tag}'
        vidispine.client.request('put', endpoint, json=shape_tag_metadata)

    return shape_tag_names


def test_list(vidispine, cassette, shape_tags):
    result = vidispine.shape_tag.list()

    assert set(shape_tags).issubset(result['uri'])
    assert cassette.all_played


def test_list_with_params(vidispine, cassette, shape_tags):
    result = vidispine.shape_tag.list({'url': True})

    assert set(shape_tags).issubset(result['uri'])
    assert cassette.all_played
