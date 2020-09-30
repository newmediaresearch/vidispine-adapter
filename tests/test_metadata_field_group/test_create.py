def test_create(vidispine, cassette):
    test_field_group_name = 'field_one'
    vidispine.metadata_field_group.create(test_field_group_name)

    assert cassette.all_played
