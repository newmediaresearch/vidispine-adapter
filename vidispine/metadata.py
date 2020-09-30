from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class MetadataField:

    def __init__(self, client) -> None:
        self.client = client

    def get(
            self,
            field_name: str,
            params: dict = {}
    ) -> BaseJson:
        if not field_name:
            raise InvalidInput("Must supply field name")

        endpoint = f'metadata-field/{field_name}'

        return self.client.get(endpoint, params=params)

    def list(self):
        endpoint = 'metadata-field/'

        return self.client.get(endpoint)
