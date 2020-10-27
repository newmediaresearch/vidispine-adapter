def test_search_shape(vidispine, cassette, item, create_shape):
    result = vidispine.search.shape()

    # We cannot assert the exact shape id as Vidispine will sometimes
    # reindex the shape id after creation.
    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played


def test_search_shape_with_params(vidispine, cassette, item, create_shape):
    result = vidispine.search.shape(params={'content': 'metadata'})

    # We cannot assert the exact shape id as Vidispine will sometimes
    # reindex the shape id after creation.
    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played


def test_search_shape_with_matrix_params(
    vidispine, cassette, item, create_shape
):
    result = vidispine.search.shape(matrix_params={'number': 10, 'first': 1})

    # We cannot assert the exact shape id as Vidispine will sometimes
    # reindex the shape id after creation.
    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played


def test_search_shape_with_params_and_matrix_params(
    vidispine, cassette, item, create_shape
):
    result = vidispine.search.shape(
        params={'content': 'metadata'}, matrix_params={'number': 10}
    )

    # We cannot assert the exact shape id as Vidispine will sometimes
    # reindex the shape id after creation.
    assert 'id' in result['shape'][0]
    assert result['shape'][0]['item'][0]['id'] == item
    assert cassette.all_played
