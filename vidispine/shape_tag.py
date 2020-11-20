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

    def get(self, shape_tag_name: str) -> BaseJson:
        """Retrieves the metadata (transcode preset) of a shape tag with
            the given tag name.

        :param shape_tag_name: The name of the shape tag.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        endpoint = self._build_url(shape_tag_name)
        return self.client.get(endpoint)

    def delete(self, shape_tag_name: str) -> None:
        """Deletes a shape tag with the given tag name.

        :param shape_tag_name: The name of the shape tag to delete.

        """
        endpoint = self._build_url(shape_tag_name)
        self.client.delete(endpoint)
