import pytest

from vidispine.errors import APIError, InvalidInput, NotFound


def test_import_to_placeholder(vidispine, cassette, item, sample_file):
    result = vidispine.item.import_to_placeholder(
        item, 'container', {'uri': sample_file}
    )

    assert result['type'] == 'PLACEHOLDER_IMPORT'
    assert cassette.all_played


def test_import_to_placeholder_not_found(vidispine, cassette, sample_file):
    with pytest.raises(NotFound) as err:
        vidispine.item.import_to_placeholder(
            'VX-1000000', 'container', {'uri': sample_file}
        )

    err.match('Not Found: POST')

    assert cassette.all_played


def test_import_to_placeholder_invalid_component(
    vidispine, cassette, item, sample_file
):
    with pytest.raises(APIError) as err:
        vidispine.item.import_to_placeholder(
            item, 'video', {'uri': sample_file}
        )

    err.match('Vidispine Error: POST')

    assert cassette.all_played


def test_import_to_placeholder_invalid_input(vidispine, item):
    with pytest.raises(InvalidInput) as err:
        vidispine.item.import_to_placeholder(
            item, 'container', {}
        )

    err.match('Please supply a URI or fileId.')
