from vidispine.errors import InvalidInput
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


class MetadataField:

    def __init__(self, client) -> None:
        self.client = client

    def get(
            self,
            field_name: str,
            params: dict = {}
    ) -> BaseJson:
        if not field_name:
            raise InvalidInput("Please supply a field name")

        endpoint = f'metadata-field/{field_name}'

        return self.client.get(endpoint, params=params)

    def list(self):
        endpoint = 'metadata-field'

        return self.client.get(endpoint)
