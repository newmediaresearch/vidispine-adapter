import pytest

from vidispine.errors import InvalidInput


@pytest.fixture
def update_shape_metadata(vidispine, cassette):
    def _update_shape_metadata(item, shape_id):
        metadata = {
            "field": [
                {
                    "key": "test",
                    "value": "test"
                }
            ]
        }
        endpoint = endpoint = f'item/{item}/shape/{shape_id}/metadata'

        vidispine.client.request('put', endpoint, json=metadata)

    return _update_shape_metadata


def test_search_shape(
        vidispine, cassette, item, create_shape, update_shape_metadata
):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    metadata = {
        "field": [
            {
                "name": "test",
                "value": [{"value": "test"}]
            }
        ]
    }

    result = vidispine.search.shape(metadata)

    assert result['hits'] > 0
    assert 'id' in result['shape'][0]
    assert 'item' in result['shape'][0]
    assert cassette.all_played


def test_search_shape_with_params(
    vidispine, cassette, item, create_shape, update_shape_metadata
):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    metadata = {
        "field": [
            {
                "name": "test",
                "value": [{"value": "test"}]
            }
        ]
    }

    result = vidispine.search.shape(metadata, params={'content': 'metadata'})

    assert result['shape'][0]['metadata']['field'][0] == {
        'key': 'test', 'value': 'test'
    }

    assert cassette.all_played


def test_search_shape_with_matrix_params(
    vidispine, cassette, item, create_shape, update_shape_metadata
):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    metadata = {
        "field": [
            {
                "name": "test",
                "value": [{"value": "test"}]
            }
        ]
    }

    result = vidispine.search.shape(
        metadata, matrix_params={'number': 10, 'first': 1}
    )

    assert result['hits'] > 0
    assert 'id' in result['shape'][0]
    assert 'item' in result['shape'][0]
    assert cassette.all_played


def test_search_shape_with_params_and_matrix_params(
    vidispine, cassette, item, create_shape, update_shape_metadata

):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    metadata = {
        "field": [
            {
                "name": "test",
                "value": [{"value": "test"}]
            }
        ]
    }

    result = vidispine.search.shape(
        metadata,
        params={'content': 'metadata'},
        matrix_params={'number': 10, 'first': 1}
    )

    assert result['shape'][0]['metadata']['field'][0] == {
        'key': 'test', 'value': 'test'
    }

    assert cassette.all_played


def test_search_shape_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.search.shape({})

    err.match('Please supply metadata.')
