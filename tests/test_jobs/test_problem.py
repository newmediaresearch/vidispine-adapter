def test_problem(vidispine, cassette):
    result = vidispine.job.problem()

    assert isinstance(result, dict)
    assert cassette.all_played
