import pytest

from vidispine.errors import NotFound


def test_add_field_to_group(
    vidispine, cassette, create_metadata_field, create_metadata_field_group
):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)

    test_field_name = 'field_one'
    create_metadata_field(test_field_name)

    vidispine.metadata_field_group.add_field_to_group(
        test_field_group_name, test_field_name
    )

    assert cassette.all_played


def test_add_field_to_group_non_existent_group(
    vidispine, cassette, create_metadata_field
):
    test_field_group_name = 'field_group1000000'

    test_field_name = 'field_one'
    create_metadata_field(test_field_name)

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.add_field_to_group(
            test_field_group_name, test_field_name
        )

    err.match('Not Found: PUT')


def test_add_field_to_group_non_existent_field(
    vidispine, cassette, create_metadata_field_group
):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)

    test_field_name = 'field1000000'

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.add_field_to_group(
            test_field_group_name, test_field_name
        )

    err.match('Not Found: PUT')
