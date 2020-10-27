from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson
from vidispine.utils import create_matrix_params_query


class Search:

    def __init__(self, client) -> None:
        self.client = client

    def __call__(self, *args, **kwargs) -> BaseJson:
        return self._search(*args, **kwargs)

    def _build_url(
        self,
        base_endpoint: str,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if params is None:
            params = {}
        if matrix_params:
            endpoint = (
                f'{base_endpoint}/{create_matrix_params_query(matrix_params)}'
            )
        else:
            endpoint = base_endpoint

        return {'endpoint': endpoint, 'params': params}

    def _search(
        self,
        metadata: dict = None,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if metadata is None:
            return self._search_without_search_doc(params, matrix_params)
        else:
            return self._search_with_search_doc(
                metadata, params, matrix_params
            )

    def _search_with_search_doc(
        self,
        metadata: dict,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if not metadata:
            raise InvalidInput('Please supply metadata.')

        url = self._build_url('search', params, matrix_params)

        return self.client.put(
            url['endpoint'], json=metadata, params=url['params']
        )

    def _search_without_search_doc(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        url = self._build_url('search', params, matrix_params)

        return self.client.get(url['endpoint'], params=url['params'])

    def shape(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        return self._search_shapes_without_search_doc(params, matrix_params)

    def _search_shapes_without_search_doc(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        url = self._build_url('search/shape', params, matrix_params)

        return self.client.get(url['endpoint'], params=url['params'])
