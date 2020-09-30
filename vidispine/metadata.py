from vidispine.typing import BaseJson


class MetadataFieldGroup:

    def __init__(self, client) -> None:
        self.client = client

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = 'metadata-field/field-group'

        return self.client.get(endpoint, params=params)
