import json
import os
import re


def test_create_placeholder(vidispine, cassette):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'dummy_placeholder_metadata.json')

    with open(filename) as f:
        metadata = json.load(f)
        result = vidispine.create_placeholder(metadata=metadata)

        assert re.match(r'^VX-\d+$', result['id'])
        assert cassette.all_played
