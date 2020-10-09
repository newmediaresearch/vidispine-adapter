def test_list(vidispine, cassette, create_collection, create_item):
    result = vidispine.search.list()

    assert 'hits' in result
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played


def test_list_with_params(vidispine, cassette, create_collection, create_item):
    result = vidispine.search.list({'content': 'metadata'})

    assert 'hits' in result
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played


def test_list_with_matrix_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search.list({}, {'number': 10, 'first': 5})

    assert 'hits' in result
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played


def test_list_with_params_and_matrix_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search.list({'content': 'metadata'}, {'number': 10})

    assert 'hits' in result
    assert 'suggestion' in result
    assert 'autocomplete' in result
    assert 'entry' in result

    assert cassette.all_played
