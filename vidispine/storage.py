import re

from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class Storage(EntityBase):
    """Manages storages

    :vidispine_docs:`Vidispine doc reference <storage/storage>`

    """
    entity = 'storage'

    def list(self, params: dict = None) -> BaseJson:
        """Lists the storages that have been configured.

        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        return self.client.get(self.entity, params=params)

    def get(self, storage_id: str) -> BaseJson:
        """Retrieves a specific storage.

        :param storage_id: The id of the storage to get.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        endpoint = self._build_url(storage_id)
        return self.client.get(endpoint)

    def create(self, metadata: dict) -> BaseJson:
        """Creates a new storage.

        :param metadata: Metadata (storage document) to create the
            storage with.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        return self.client.post(self.entity, json=metadata)

    def update(self, storage_id: str, metadata: dict) -> BaseJson:
        """Updates an existing storage.

        :param storage_id: The id of the storage to get.
        :param metadata: Metadata (storage document) of the storage to
            update.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = self._build_url(storage_id)

        return self.client.put(endpoint, json=metadata)

    def delete(self, storage_id: str, params: dict = None) -> None:
        """Deletes the storage.

        :param storage_id: The id of the storage to delete.
        :param params: Optional query params.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(storage_id)
        self.client.delete(endpoint, params=params)

    def add_storage_method(
        self,
        storage_id: str,
        method_id: str,
        params: dict
    ) -> BaseJson:
        """Adds a new access method to the storage.

        :param storage_id: The id of the storage to add the method to.
        :param method_id: The id of the method to add to the storage.
        :param params: Optional query params.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        return self._update_storage_method(storage_id, method_id, params)

    def update_storage_method(
        self,
        storage_id: str,
        method_id: str,
        params: dict
    ) -> BaseJson:
        """Updates an existing access method on a storage.

        :param storage_id: The id of the storage with the method to
            update.
        :param method_id: The id of the method to update.
        :param params: Optional query params.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        return self._update_storage_method(storage_id, method_id, params)

    def _update_storage_method(
        self,
        storage_id: str,
        method_id: str,
        params: dict
    ) -> BaseJson:

        headers = {'accept': 'text/plain'}
        endpoint = self._build_url(f'{storage_id}/method/{method_id}')

        plain_text_response = self.client.put(
            endpoint, headers=headers, params=params
        )
        storage_url = params['url']

        return {
            'method_id': re.match(  # type: ignore
                method_id, plain_text_response
            ).group(0),
            'storage_url': re.search(  # type: ignore
                storage_url, plain_text_response
            ).group(0)
        }

    def get_storage_method(
        self,
        storage_id: str,
        method_id: str,
        params: dict = None,
    ) -> BaseJson:
        """Retrieves the access methods configured on a specific storage.

        :param storage_id: The id of the storage with the method to get.
        :param method_id: The id of the method to update.
        :param params: Optional query params.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(f'{storage_id}/method/{method_id}')

        return self.client.get(endpoint, params=params)
