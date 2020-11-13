import re

import pytest

from vidispine.errors import InvalidInput, NotFound
from vidispine.utils import generate_metadata


def test_update_collection(
    vidispine, cassette, create_metadata_field, collection
):
    create_metadata_field('field_one')
    create_metadata_field('field_two')

    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123
    }

    vidispine.collection.update_metadata(collection, generate_metadata(fields))

    assert cassette.all_played


def test_update_collection_field_does_not_exist(
    vidispine, cassette, create_metadata_field, collection
):
    create_metadata_field('field_one')
    create_metadata_field('field_two')

    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123,
        'field_three': 'stuff'
    }

    with pytest.raises(NotFound) as err:
        vidispine.collection.update_metadata(
            collection, generate_metadata(fields)
        )

        re.match(
            r'Endpoint not found: PUT'
            r' - http://localhost:8080/API/collection/VX-\d+$/metadata', err
        )

    assert cassette.all_played


def test_update_collection_collection_not_found(vidispine, cassette):
    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123
    }

    with pytest.raises(NotFound) as err:
        vidispine.collection.update_metadata(
            'VX-1000000', generate_metadata(fields)
        )

    err.match(r'Not Found: PUT')

    assert cassette.all_played


def test_update_collection_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.collection.update_metadata('VX-1000000', {})

    err.match('Please supply metadata.')


def test_update_item(
    vidispine, cassette, create_metadata_field, item
):

    create_metadata_field('field_one')
    create_metadata_field('field_two')

    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123
    }

    vidispine.item.update_metadata(item, generate_metadata(fields))

    assert cassette.all_played


def test_update_item_field_does_not_exist(
    vidispine, cassette, create_metadata_field, item
):
    create_metadata_field('field_one')
    create_metadata_field('field_two')

    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123,
        'field_three': 'stuff'
    }

    with pytest.raises(NotFound) as err:
        vidispine.item.update_metadata(
            item, generate_metadata(fields)
        )

        re.match(
            r'Endpoint not found: PUT'
            r' - http://localhost:8080/API/item/VX-\d+$/metadata', err
        )

    assert cassette.all_played


def test_update_item_item_not_found(vidispine, cassette):
    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123
    }

    with pytest.raises(NotFound) as err:
        vidispine.item.update_metadata(
            'VX-1000000', generate_metadata(fields)
        )

    err.match(r'Not Found: PUT')

    assert cassette.all_played


def test_update_item_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.item.update_metadata('VX-1000000', {})

    err.match('Please supply metadata.')
