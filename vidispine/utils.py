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


def create_matrix_params_query(matrix_params: dict) -> str:
    return ';' + ';'.join(
        f'{key}={value}' for key, value in matrix_params.items()
    )
