

class MetadataField:

    def __init__(self, client) -> None:
        self.client = client

    def delete(self, field_name: str) -> None:
        endpoint = f'metadata-field/{field_name}'
        self.client.delete(endpoint)
