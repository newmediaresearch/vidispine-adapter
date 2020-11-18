from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class Storage(EntityBase):
    """Manages storages

    :vidispine_docs:`Vidispine doc reference <storage/storage>`

    """
    entity = 'storage'

    def update(self, storage_id: str, metadata: dict) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = self._build_url(storage_id)

        return self.client.put(endpoint, json=metadata)
