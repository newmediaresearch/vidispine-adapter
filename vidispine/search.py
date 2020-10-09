from vidispine.typing import BaseJson
from vidispine.utils import create_matrix_params_query


class Search:

    def __init__(self, client) -> None:
        self.client = client

    def list(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        endpoint = 'search'

        if params is None:
            params = {}
        if matrix_params:
            endpoint += create_matrix_params_query(matrix_params)

        return self.client.get(endpoint, params=params)
