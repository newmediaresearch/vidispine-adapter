from vidispine.base import EntityBase
from vidispine.errors import InvalidInput


class ShapeTag(EntityBase):
    """Shape tags

    Manage shape tags.

    :vidispine_docs:`Vidispine doc reference <shape-tag>`

    """
    entity = 'shape-tag'

    def create(self, shape_tag_name: str, metadata: dict) -> None:
        """Creates a new shape tag with the given tag name.

        :param shape_tag_name: The name of the shape tag to create.
        :param metadata: The metadata (transcode preset document) to
            create the shape tag with.

        """
        self._update(shape_tag_name, metadata)

    def update(self, shape_tag_name: str, metadata: dict) -> None:
        """Updates a shape tag with the given tag name.

        :param shape_tag_name: The name of the shape tag to update.
        :param metadata: The metadata (transcode preset document) to
            update the shape tag with.

        """
        self._update(shape_tag_name, metadata)

    def _update(self, shape_tag_name: str, metadata: dict) -> None:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = self._build_url(shape_tag_name)

        self.client.put(endpoint, json=metadata)
