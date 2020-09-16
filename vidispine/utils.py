def generate_metadata(fields: dict) -> dict:
    metadata = {
        "timespan": [{
            "field": [{
                "name": key,
                "value": [{"value": value}]
            }
                for key, value in fields.items()
            ],
            "start": "-INF",
            "end": "+INF"
        }]
    }

    return metadata
