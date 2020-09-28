from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class MetadataField:

    def __init__(self, client) -> None:
        self.client = client

    def update(self, metadata: dict, field_name: str) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = f'metadata-field/{field_name}'

        return self.client.put(endpoint, json=metadata)
