import re


def test_create_placeholder(vidispine, cassette):
    metadata = {
        "timespan": [{
            "field": [{
                "name": "title",
                "value": [{
                    "value": "My placeholder import!"
                }]
            }],
            "start": "-INF",
            "end": "+INF"
        }]
    }

    result = vidispine.create_placeholder(metadata=metadata)

    assert re.match(r'^VX-\d+$', result['id'])
    assert cassette.all_played
