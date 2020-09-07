

class Collection:

    def __init__(self, client):
        self.client = client

    def create(self, name):
        params = {'name': name}

        response = self.client.post('collection', params=params).json()

        return response['id']
