import pytest

from vidispine.errors import InvalidInput, NotFound


def test_import_shape(vidispine, cassette, create_item, sample_file):
    result = vidispine.item_shape.import_shape(
        create_item, {'uri': sample_file}
    )

    assert result['type'] == 'SHAPE_IMPORT'
    assert cassette.all_played


def test_import_item_not_found(vidispine, cassette, sample_file):
    with pytest.raises(NotFound) as err:
        vidispine.item_shape.import_shape('VX-1000000', {'uri': sample_file})

    err.match('Not Found: POST')

    assert cassette.all_played


def test_import_invalid_input(vidispine, create_item):
    with pytest.raises(InvalidInput) as err:
        vidispine.item_shape.import_shape(create_item, {})

    err.match('Please supply a URI or fileId.')
