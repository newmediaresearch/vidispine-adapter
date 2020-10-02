import pytest

from vidispine.errors import NotFound


def test_add_group_to_group(vidispine, cassette, create_metadata_field_group):
    parent_group = 'field_one'
    child_group = 'field_one_child'
    create_metadata_field_group(parent_group)
    create_metadata_field_group(child_group)

    vidispine.metadata_field_group.add_group_to_group(
        parent_group, child_group
    )

    assert cassette.all_played


def test_add_group_to_group_non_existent_parent_group(
    vidispine, cassette, create_metadata_field_group
):
    parent_group = 'field1000000'
    child_group = 'field_one_child'
    create_metadata_field_group(child_group)

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.add_group_to_group(
            parent_group, child_group
        )

    err.match(r'Not Found: PUT')

    assert cassette.all_played


def test_add_group_to_group_non_existent_child_group(
    vidispine, cassette, create_metadata_field_group
):
    parent_group = 'field_one'
    child_group = 'field1000000'
    create_metadata_field_group(parent_group)

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.add_group_to_group(
            parent_group, child_group
        )

    err.match(r'Not Found: PUT')

    assert cassette.all_played
