class MetadataFieldGroup:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, field_group_name: str, params: dict = None) -> None:
        if params is None:
            params = {}

        endpoint = f'metadata-field/field-group/{field_group_name}'

        self.client.put(endpoint, params=params)
