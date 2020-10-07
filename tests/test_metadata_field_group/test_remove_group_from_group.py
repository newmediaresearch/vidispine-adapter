import pytest

from vidispine.errors import NotFound


def test_remove_group_from_group(
    vidispine, cassette, create_metadata_field_group
):
    parent_group = 'field_one'
    child_group = 'field_one_child'
    create_metadata_field_group(parent_group)
    create_metadata_field_group(child_group)

    endpoint = (
        f'/metadata-field/field-group/{parent_group}/group/{child_group}'
    )
    vidispine.client.request('put', endpoint)

    vidispine.metadata_field_group.remove_group_from_group(
        parent_group, child_group
    )

    assert cassette.all_played


def test_remove_group_from_group_non_existent_parent_group(
    vidispine, cassette
):
    parent_group = 'field1000000'
    child_group = 'field_one_child'

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.remove_group_from_group(
            parent_group, child_group
        )

    err.match('Not Found: DELETE')

    assert cassette.all_played


def test_remove_group_from_group_non_existent_child_group(
    vidispine, cassette, create_metadata_field_group
):
    parent_group = 'field_one'
    child_group = 'field1000000'
    create_metadata_field_group(parent_group)

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.remove_group_from_group(
            parent_group, child_group
        )

    err.match('Not Found: DELETE')

    assert cassette.all_played
