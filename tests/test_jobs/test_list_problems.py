def test_list_problems(vidispine, cassette):
    result = vidispine.job.list_problems()

    assert isinstance(result, dict)
    assert cassette.all_played
