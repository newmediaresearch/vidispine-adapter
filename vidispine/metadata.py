from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class MetadataFieldGroup:

    def __init__(self, client) -> None:
        self.client = client

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = 'metadata-field/field-group'

        return self.client.get(endpoint, params=params)

    def add_field_to_group(
        self,
        field_group_name: str,
        field_name: str
    ) -> None:

        endpoint = (
            'metadata-field/field-group/'
            f'{field_group_name}/{field_name}'
        )

        self.client.put(endpoint)


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
