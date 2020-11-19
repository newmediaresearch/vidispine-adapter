from vidispine.base import EntityBase
from vidispine.typing import BaseJson


class Storage(EntityBase):
    """Manages storages

    :vidispine_docs:`Vidispine doc reference <storage/storage>`

    """
    entity = 'storage'

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        return self.client.get(self.entity)
