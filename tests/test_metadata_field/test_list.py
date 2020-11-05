def test_list_metadata_returns_all_fields(cassette, vidispine):
    metadata = vidispine.metadata_field.list()

    assert metadata['field']
    assert cassette.all_played


def test_list_metadata_returns_all_fields_with_params(cassette, vidispine):
    metadata = vidispine.metadata_field.list({'includeVales': True})

    assert metadata['field']
    assert cassette.all_played
