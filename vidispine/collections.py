
class Collection:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, name: str) -> str:
        params = {'name': name}

        response = self.client.post('collection', params=params).json()

        return response['id']

    def get(self, _id: str, metadata: bool = True) -> dict:
        if metadata:
            endpoint = f'collection/{_id}/metadata'
        else:
            endpoint = f'collection/{_id}'

        response = self.client.get(endpoint).json()

        return response
