from vidispine.client import Client, Vidispine


def test_vidispine_init():
    vidispine = Vidispine('http://localhost:8080', 'admin', 'admin')

    assert isinstance(vidispine.client, Client)


def test_version(cassette, vidispine):
    version_data = vidispine.version()

    assert version_data['component'][0]['name'] == 'API'
    assert cassette.play_count == 1

def test_get_item(cassette, vidispine):
    vidispine = Vidispine('http://192.168.9.60:8080', 'admin', 'admin')
    item = vidispine.get_item(item_id='VX-12')

    assert item['id'] == 'VX-12'

    # assert these keys have been returned
    assert item['metadata']
    assert item['files']