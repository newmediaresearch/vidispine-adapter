from vidispine.typing import BaseJson
from vidispine.utils import create_matrix_params_query


class Search:

    def __init__(self, client) -> None:
        self.client = client

    def list_shapes(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        endpoint = 'search/shape'

        if params is None:
            params = {}
        if matrix_params:
            endpoint += create_matrix_params_query(matrix_params)

        return self.client.get(endpoint, params=params)
