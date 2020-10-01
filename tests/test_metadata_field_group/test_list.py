
def test_list(vidispine, cassette, metadata_field_group):
    result = vidispine.metadata_field_group.list()
    field_group_names = [group['name'] for group in result['group']]

    assert metadata_field_group in field_group_names
    assert cassette.all_played


def test_list_with_content(vidispine, cassette, metadata_field_group):
    result = vidispine.metadata_field_group.list({'content': True})
    field_group_names = [group['name'] for group in result['group']]

    assert metadata_field_group in field_group_names
    assert 'schema' in result['group'][0]
    assert cassette.all_played
