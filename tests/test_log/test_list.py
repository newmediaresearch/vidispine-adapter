import time


def test_list(vidispine, cassette):
    result = vidispine.log.list()['entry']

    fields = ['username', 'method', 'path', 'timestamp']

    assert all(field in result[0] for field in fields)
    assert cassette.all_played


def test_list_with_path(vidispine, cassette, create_item):
    item_id = create_item

    # Give Vidipsine enough time to update the logs.
    if cassette.dirty:
        time.sleep(2)

    result = vidispine.log.list(
        params={'path': f'/item/{item_id}'}
    )['entry']

    fields = ['username', 'method', 'path', 'timestamp']

    assert all(field in result[0] for field in fields)
    assert item_id in result[0]['path']
    assert cassette.all_played
