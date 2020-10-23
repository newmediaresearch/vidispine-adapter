def test_search(vidispine, cassette, create_collection, create_item):
    result = vidispine.search()

    assert result['hits'] > 2
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played


def test_search_with_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search(params={'content': 'metadata'})

    assert result['hits'] > 2
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played


def test_search_with_matrix_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search(matrix_params={'number': 10, 'first': 1})

    assert result['hits'] > 2
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played


def test_search_with_params_and_matrix_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search(
        params={'content': 'metadata'}, matrix_params={'number': 10}
    )

    assert result['hits'] > 2
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played
