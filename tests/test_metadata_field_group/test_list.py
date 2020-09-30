def test_list(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)

    result = vidispine.metadata_field_group.list()
    field_group_names = [group['name'] for group in result['group']]

    assert test_field_group_name in field_group_names
    assert cassette.all_played


def test_list_with_content(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)

    result = vidispine.metadata_field_group.list({'content': True})
    field_group_names = [group['name'] for group in result['group']]

    assert test_field_group_name in field_group_names
    assert 'schema' in result['group'][0]
    assert cassette.all_played
