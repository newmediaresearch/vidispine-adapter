
class Item:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, name: str) -> str:
        params = {
            'name': name
        }

        endpoint = f'{self.client.base_url}item/'
        response = self.client.post(endpoint, params=params).json()

        return response['id']

    def get(self, item_id: str, metadata=True) -> dict:
        if metadata:
            params = {
                'content': 'metadata'
            }
        else:
            params = {}

        endpoint = f'{self.client.base_url}item/{item_id}'

        return self.client.get(endpoint, params=params).json()