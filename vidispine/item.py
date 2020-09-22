class Item:

    def __init__(self, client) -> None:
        self.client = client

    def create_placeholder(self, metadata: dict, params: dict = None) -> dict:
        if params is None:
            params = {}

        params.setdefault('container', 1)

        endpoint = 'import/placeholder'

        return self.client.post(
            endpoint, payload=metadata, params=params
        ).json()
