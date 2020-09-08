from vidispine.client import Vidispine, Client


def test_vidispine_init():
    vidispine = Vidispine('http://localhost', 'admin', 'admin')

    assert isinstance(vidispine.client, Client)


def test_version(cassette, vidispine):
    version_data = vidispine.version()

    assert version_data['component'][0]['name'] == 'API'
    assert cassette.play_count == 1
