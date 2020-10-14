def test_list_shapes(vidispine, cassette):
    result = vidispine.search.list_shapes()

    assert 'hits' in result
    assert 'shape' in result
    assert cassette.all_played


def test_list_shapes_with_params(vidispine, cassette):
    result = vidispine.search.list_shapes({'content': 'metadata'})

    assert 'hits' in result
    assert 'shape' in result
    assert cassette.all_played


def test_list_shapes_with_matrix_params(vidispine, cassette):
    result = vidispine.search.list_shapes({}, {'number': 10, 'first': 5})

    assert 'hits' in result
    assert 'shape' in result
    assert cassette.all_played


def test_list_shapes_with_params_and_matrix_params(vidispine, cassette):
    result = vidispine.search.list_shapes(
        {'content': 'metadata'}, {'number': 10}
    )

    assert 'hits' in result
    assert 'shape' in result
    assert cassette.all_played
