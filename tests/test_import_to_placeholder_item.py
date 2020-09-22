import os

import pytest

from vidispine.errors import NotFound, APIError


@pytest.fixture
def sample_file():
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, 'sample-mp4-file.mp4')

    return file


def test_import_to_placeholder_item(vidispine, cassette, sample_file):
    vidispine.import_to_placeholder_item(
        'VX-14', 'container', {'uri': sample_file}
    )

    assert cassette.all_played


def test_import_to_placeholder_item_not_found(
    vidispine, cassette, sample_file
):
    with pytest.raises(NotFound) as err:
        vidispine.import_to_placeholder_item(
            'VX-1000000', 'container', {'uri': sample_file}
        )

    err.match(
        r'Endpoint not found: POST'
        r' - http://localhost:8080/API/import/placeholder/VX-1000000/'
    )

    assert cassette.all_played


def test_import_to_placeholder_item_invalid_input(
    vidispine, cassette, sample_file
):
    with pytest.raises(APIError) as err:
        vidispine.import_to_placeholder_item(
            'VX-14', 'video', {'uri': sample_file}
        )

    err.match(
        r'Vidispine Error: POST'
        r' - http://localhost:8080/API/import/placeholder/VX-'
    )
