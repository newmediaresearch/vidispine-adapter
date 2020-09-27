from vidispine.typing import BaseJson


class Metadata:

    def __init__(self, client) -> None:
        self.client = client

    def get(
        self,
        field_name: str = '',
    ) -> BaseJson:

        endpoint = f'metadata-field/{field_name}'

        return self.client.get(endpoint)
