import pytest

from vidispine.errors import NotFound


def test_remove_field_from_group(
    vidispine, cassette, create_metadata_field_group
):

    test_field_group_name = create_metadata_field_group
    test_field_name = 'field_one'

    endpoint = (
        'metadata-field/field-group/'
        f'{test_field_group_name}/{test_field_name}'
    )
    vidispine.client.request('put', endpoint)

    vidispine.metadata_field_group.remove_field_from_group(
        test_field_group_name, test_field_name
    )

    assert cassette.all_played


def test_non_existent_metadata_field_group(vidispine, cassette):
    test_field_group_name = 'field_group1000000'
    test_field_name = 'field_one'

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.remove_field_from_group(
            test_field_group_name, test_field_name
        )

    err.match('Not Found: DELETE')

    assert cassette.all_played


def test_non_existent_field_in_group(
    vidispine, cassette, create_metadata_field_group
):
    test_field_group_name = create_metadata_field_group
    test_field_name = 'field1000000'

    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.remove_field_from_group(
            test_field_group_name, test_field_name
        )

    err.match('Not Found: DELETE')

    assert cassette.all_played
