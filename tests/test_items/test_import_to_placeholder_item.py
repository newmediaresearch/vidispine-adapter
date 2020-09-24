import os
import re

import pytest

from vidispine.errors import APIError, InvalidInput, NotFound


@pytest.fixture
def sample_file():
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, 'sample-mp4-file.mp4')

    return file


def test_import_to_placeholder_item(
    vidispine, cassette, create_item, sample_file
):
    vidispine.item.import_to_placeholder_item(
        create_item, 'container', {'uri': sample_file}
    )

    assert cassette.all_played


def test_import_to_placeholder_item_not_found(
    vidispine, cassette, sample_file
):
    with pytest.raises(NotFound) as err:
        vidispine.item.import_to_placeholder_item(
            'VX-1000000', 'container', {'uri': sample_file}
        )

    err.match(
        r'Endpoint not found: POST'
        r' - http://localhost:8080/API/import/placeholder/VX-1000000/'
    )

    assert cassette.all_played


def test_import_to_placeholder_item_invalid_component(
    vidispine, cassette, create_item, sample_file
):
    with pytest.raises(APIError) as err:
        vidispine.item.import_to_placeholder_item(
            create_item, 'video', {'uri': sample_file}
        )

        re.match(
            r'Vidispine Error: POST'
            r' - http://localhost:8080/API/import/placeholder/VX-\d+$/', err
        )

    assert cassette.all_played


def test_import_to_placeholder_item_invalid_input(vidispine, create_item):
    with pytest.raises(InvalidInput) as err:
        vidispine.item.import_to_placeholder_item(
            create_item, 'container', {}
        )

    err.match('Please supply a URI or fileId.')
