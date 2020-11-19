from vidispine.base import EntityBase
from vidispine.typing import BaseJson


class Storage(EntityBase):
    """Manages storages

    :vidispine_docs:`Vidispine doc reference <storage/storage>`

    """
    entity = 'storage'

    def get(self, storage_id: str) -> BaseJson:
        """Retrieves a specific storage.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        endpoint = self._build_url(storage_id)
        return self.client.get(endpoint)
