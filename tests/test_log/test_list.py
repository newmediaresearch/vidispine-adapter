import time


def test_list(vidispine, cassette):
    result = vidispine.log.list()['entry']

    assert 'username' in result[0]
    assert 'method' in result[0]
    assert 'path' in result[0]
    assert 'timestamp' in result[0]
    assert cassette.all_played


def test_list_with_path(vidispine, cassette, item):
    # Give Vidipsine enough time to update the logs.
    if cassette.dirty:
        time.sleep(2)

    result = vidispine.log.list(
        params={'path': f'/item/{item}'}
    )['entry']

    assert 'username' in result[0]
    assert 'method' in result[0]
    assert 'path' in result[0]
    assert 'timestamp' in result[0]
    assert item in result[0]['path']
    assert cassette.all_played
