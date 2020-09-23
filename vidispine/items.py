
class Item:

    def __init__(self, client) -> None:
        self.client = client

    def get(self, item_id: str, params: dict = None, metadata=True) -> dict:
        if not params:
            params = {}

        if metadata:
            params.setdefault('content', 'metadata')

        endpoint = f'item/{item_id}'

        return self.client.get(endpoint, params=params)
