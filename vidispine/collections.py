
class Collection:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, name: str) -> str:
        params = {'name': name}

        response = self.client.post('collection', params=params).json()

        return response['id']

    def get(self, vidispine_id: str, metadata: bool = True) -> dict:
        if metadata:
            endpoint = f'collection/{vidispine_id}/metadata'
        else:
            endpoint = f'collection/{vidispine_id}'

        return self.client.get(endpoint).json()

    def delete(self, vidispine_id: str) -> None:
        endpoint = f'collection/{vidispine_id}'

        self.client.delete(endpoint)

    def update(self, vidispine_id: str, metadata: dict) -> dict:
        endpoint = f'collection/{vidispine_id}/metadata'

        return self.client.put(endpoint, payload=metadata).json()

    def list(self, params: dict = None) -> dict:
        endpoint = 'collection'

        return self.client.get(endpoint, params=params).json()
