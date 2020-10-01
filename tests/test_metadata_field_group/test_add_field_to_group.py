import pytest

from vidispine.errors import NotFound


def test_add_field_to_group(
    vidispine, cassette, metadata_field, metadata_field_group
):
    vidispine.metadata_field_group.add_field_to_group(
        metadata_field_group, metadata_field
    )

    assert cassette.all_played


def test_add_field_to_group_non_existent_group(
    vidispine, cassette, metadata_field
):
    test_field_group_name = 'field_group1000000'

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.add_field_to_group(
            test_field_group_name, metadata_field
        )

    err.match('Not Found: PUT')

    assert cassette.all_played


def test_add_field_to_group_non_existent_field(
    vidispine, cassette, metadata_field_group
):
    test_field_name = 'field1000000'

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.add_field_to_group(
            metadata_field_group, test_field_name
        )

    err.match('Not Found: PUT')

    assert cassette.all_played
