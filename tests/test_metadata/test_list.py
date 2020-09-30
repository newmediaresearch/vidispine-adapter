def test_list_metadata_returns_all_fields(cassette, vidispine):
    metadata = vidispine.metadata.list()

    assert metadata['field']
    assert cassette.all_played
