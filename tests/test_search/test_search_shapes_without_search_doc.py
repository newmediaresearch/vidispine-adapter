def test_search_shape(vidispine, cassette, item, create_shape):
    create_shape(item)

    result = vidispine.search.shape()

    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played


def test_search_shape_with_params(vidispine, cassette, item, create_shape):
    create_shape(item)

    result = vidispine.search.shape(params={'content': 'metadata'})

    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played


def test_search_shape_with_matrix_params(
    vidispine, cassette, item, create_shape
):
    create_shape(item)

    result = vidispine.search.shape(matrix_params={'number': 10, 'first': 1})

    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played


def test_search_shape_with_params_and_matrix_params(
    vidispine, cassette, item, create_shape
):

    create_shape(item)

    result = vidispine.search.shape(
        params={'content': 'metadata'}, matrix_params={'number': 10}
    )

    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played
