from vidispine.base import EntityBase
from vidispine.typing import BaseJson


class Log(EntityBase):

    entity = 'log'

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        return self.client.get(self.entity, params=params)
