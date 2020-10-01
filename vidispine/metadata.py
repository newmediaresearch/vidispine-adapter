from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class MetadataFieldGroup:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, field_group_name: str, params: dict = None) -> None:
        if params is None:
            params = {}

        endpoint = f'metadata-field/field-group/{field_group_name}'

        self.client.put(endpoint, params=params)

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = 'metadata-field/field-group'

        return self.client.get(endpoint, params=params)

    def delete(self, field_group_name: str) -> None:
        endpoint = f'metadata-field/field-group/{field_group_name}'
        self.client.delete(endpoint)


class MetadataField:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, metadata: dict, field_name: str) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = f'metadata-field/{field_name}'

        return self.client.put(endpoint, json=metadata)

    def update(self, metadata: dict, field_name: str) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = f'metadata-field/{field_name}'

        return self.client.put(endpoint, json=metadata)

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

    def delete(self, field_name: str) -> None:
        endpoint = f'metadata-field/{field_name}'
        self.client.delete(endpoint)
