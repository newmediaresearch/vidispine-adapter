
class Item:

    def __init__(self, client) -> None:
        self.client = client

    def get(self, item_id: str, params: dict = {}, metadata=True) -> dict:

        if metadata:
            params.update(
                {'content': 'metadata'}
            )
        else:
            params.update(
                {'content': ''}
            )

        endpoint = f'{self.client.base_url}item/{item_id}'

        return self.client.get(endpoint, params=params).json()
