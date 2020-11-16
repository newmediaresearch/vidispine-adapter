from vidispine.base import EntityBase
from vidispine.typing import BaseJson


class ShapeTag(EntityBase):
    """Shape tags

    Manage shape tags.

    :vidispine_docs:`Vidispine doc reference <shape-tag>`

    """
    entity = 'shape-tag'

    def list(self, params: dict = None) -> BaseJson:
        """Retrieves all shape tags known by the system.

        :param params: Optional query params.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        return self.client.get(self.entity)
