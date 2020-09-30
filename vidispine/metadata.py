from vidispine.typing import BaseJson


class MetadataField:

    def __init__(self, client) -> None:
        self.client = client

    def delete(self, field_name: str) -> None:
        endpoint = f'metadata-field/{field_name}'
        self.client.delete(endpoint)


class MetadataFieldGroup:

    def __init__(self, client) -> None:
        self.client = client

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = 'metadata-field/field-group'

        return self.client.get(endpoint, params=params)
