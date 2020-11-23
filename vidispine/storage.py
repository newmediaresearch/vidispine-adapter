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
