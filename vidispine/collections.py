from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class Collection(EntityBase):
    """Collections

    A collection is an ordered logical set of items, libraries and
    other collections.

    """
    entity = 'collection'

    def create(self, params: dict = None) -> str:
        if params is None:
            params = {}

        response = self.client.post(self.entity, params=params)

        return response['id']

    def get(self, vidispine_id: str, metadata: bool = True) -> BaseJson:
        if metadata:
            endpoint = self._build_url(f'{vidispine_id}/metadata')
        else:
            endpoint = self._build_url(vidispine_id)

        return self.client.get(endpoint)

    def delete(self, vidispine_id: str) -> None:
        endpoint = self._build_url(vidispine_id)

        self.client.delete(endpoint)

    def delete_multiple(self, vidispine_ids: list) -> None:
        if not vidispine_ids:
            raise InvalidInput('Please supply Vidispine IDs to delete.')

        params = {'id': ','.join(vidispine_ids)}

        self.client.delete(self.entity, params=params)

    def update_metadata(self, vidispine_id: str, metadata: dict) -> BaseJson:
        endpoint = self._build_url(f'{vidispine_id}/metadata')

        return self.client.put(endpoint, json=metadata)

    def list(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        endpoint = self._build_url(matrix_params=matrix_params)

        return self.client.get(endpoint, params=params)
