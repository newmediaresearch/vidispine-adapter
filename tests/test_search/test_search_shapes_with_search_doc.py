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


@pytest.fixture
def shape_search_metadata():
    return {
        "field": [
            {
                "name": "test",
                "value": [{"value": "test"}]
            }
        ]
    }


def test_search_shape(
    vidispine,
    cassette,
    item,
    create_shape,
    update_shape_metadata,
    shape_search_metadata
):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    result = vidispine.search.shape(shape_search_metadata)

    assert result['hits'] > 0
    assert 'id' in result['shape'][0]
    assert 'item' in result['shape'][0]
    assert cassette.all_played


def test_search_shape_with_params(
    vidispine,
    cassette,
    item,
    create_shape,
    update_shape_metadata,
    shape_search_metadata
):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    result = vidispine.search.shape(
        shape_search_metadata, params={'content': 'metadata'}
    )

    expected_shape = {
        "id": shape_id,
        "item": [{"id": item}],
        "metadata": {
            "field": [
                {
                    "key": "test",
                    "value": "test"
                }
            ]
        },
    }
    assert expected_shape in result['shape']
    assert cassette.all_played


def test_search_shape_with_matrix_params(
    vidispine,
    cassette,
    item,
    create_shape,
    update_shape_metadata,
    shape_search_metadata
):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    result = vidispine.search.shape(
        shape_search_metadata, matrix_params={'number': 10, 'first': 1}
    )

    assert result['hits'] > 0
    assert 'id' in result['shape'][0]
    assert 'item' in result['shape'][0]
    assert cassette.all_played


def test_search_shape_with_params_and_matrix_params(
    vidispine,
    cassette,
    item,
    create_shape,
    update_shape_metadata,
    shape_search_metadata

):
    shape_id = create_shape(item)
    update_shape_metadata(item, shape_id)

    result = vidispine.search.shape(
        shape_search_metadata,
        params={'content': 'metadata'},
        matrix_params={'number': 10, 'first': 1}
    )

    expected_shape = {
        "id": shape_id,
        "item": [{"id": item}],
        "metadata": {
            "field": [
                {
                    "key": "test",
                    "value": "test"
                }
            ]
        },
    }
    assert expected_shape in result['shape']
    assert cassette.all_played


def test_search_shape_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.search.shape({})

    err.match('Please supply metadata.')
