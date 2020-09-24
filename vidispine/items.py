from vidispine.typing import BaseJson


class Item:

    def __init__(self, client) -> None:
        self.client = client

    def get(
        self,
        item_id: str,
        params: dict = None,
        metadata=True
    ) -> BaseJson:
        if not params:
            params = {}

        if metadata:
            params.setdefault('content', 'metadata')

        endpoint = f'item/{item_id}'

        return self.client.get(endpoint, params=params)

    def delete(self, item_id: str) -> None:
        endpoint = f'item/{item_id}'
        self.client.delete(endpoint)

    def create_placeholder(
        self,
        metadata: dict,
        params: dict = None
    ) -> BaseJson:
        if params is None:
            params = {}

        params.setdefault('container', 1)

        endpoint = 'import/placeholder'

        return self.client.post(
            endpoint, json=metadata, params=params
        )
