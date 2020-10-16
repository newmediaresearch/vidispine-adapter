def test_search(vidispine, cassette, create_collection, create_item):
    result = vidispine.search()['entry']

    assert len(result[0])
    assert len(result[1])

    assert cassette.all_played


def test_search_with_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search(params={'content': 'metadata'})['entry']

    assert len(result[0])
    assert len(result[1])

    assert cassette.all_played


def test_search_with_matrix_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search(
        matrix_params={'number': 10, 'first': 1}
    )['entry']

    assert len(result[0])
    assert len(result[1])

    assert cassette.all_played


def test_search_with_params_and_matrix_params(
    vidispine, cassette, create_collection, create_item
):
    result = vidispine.search(
        params={'content': 'metadata'}, matrix_params={'number': 10}
    )['entry']

    assert len(result[0])
    assert len(result[1])

    assert cassette.all_played
