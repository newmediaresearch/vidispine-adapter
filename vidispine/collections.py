from .client import Client

class Collection:

    def __init__(self, client: Client) -> None:
        self.client = client

    def create(self, name: str) -> str:
        params = {'name': name}

        response = self.client.post('collection', params=params).json()

        return response['id']
