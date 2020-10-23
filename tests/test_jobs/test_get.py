import pytest

from vidispine.errors import NotFound


def test_get(vidispine, cassette, item, sample_file):
    endpoint = f'import/placeholder/{item}/container'
    params = {'uri': sample_file}
    job_id = vidispine.client.post(endpoint, params=params)['jobId']

    result = vidispine.job.get(job_id)

    assert result['jobId'] == job_id
    assert cassette.all_played


def test_get_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.job.get('VX-1000000')

    err.match(r'Not Found: GET')

    assert cassette.all_played
