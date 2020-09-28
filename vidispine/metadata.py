from vidispine.typing import BaseJson
from vidispine.errors import InvalidInput


class MetadataField:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, metadata: dict, field_name: str) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = f'metadata-field/{field_name}'

        return self.client.put(endpoint, json=metadata)
