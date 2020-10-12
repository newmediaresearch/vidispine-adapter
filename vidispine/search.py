from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson
from vidispine.utils import create_matrix_params_query


class Search:

    def __init__(self, client) -> None:
        self.client = client

    def list_from_metadata(
        self,
        metadata: dict,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = 'search'

        if params is None:
            params = {}
        if matrix_params:
            endpoint += create_matrix_params_query(matrix_params)

        return self.client.get(endpoint, json=metadata, params=params)
