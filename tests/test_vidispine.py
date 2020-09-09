from vidispine.client import Client, Vidispine


def test_vidispine_init():
    vidispine = Vidispine('http://localhost:8080', 'admin', 'admin')

    assert isinstance(vidispine.client, Client)


def test_version(cassette, vidispine):
    version_data = vidispine.version()

    assert version_data['component'][0]['name'] == 'API'
    assert cassette.all_played
