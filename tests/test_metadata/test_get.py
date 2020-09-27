def test_get_metadata_returns_all_fields(cassette, vidispine):
    field_name = ''

    metadata = vidispine.metadata.get(field_name)

    assert metadata['field']
    assert cassette.all_played


def test_get_metadata_returns_single_field(cassette, vidispine):
    field_name = 'durationTimeCode'

    metadata = vidispine.metadata.get(field_name)

    assert not metadata.get('field')  # not all fields returned
    assert metadata['name'] == field_name
    assert cassette.all_played
