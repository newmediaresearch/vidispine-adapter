from vidispine.base import EntityBase


class ShapeTag(EntityBase):
    """Shape tags

    Manage shape tags.

    :vidispine_docs:`Vidispine doc reference <shape-tag>`

    """
    entity = 'shape-tag'

    def delete(self, shape_tag_name: str) -> None:
        """Deletes a shape tag with the given tag name.

        :param shape_tag_name: The name of the shape tag to delete.

        """
        endpoint = self._build_url(shape_tag_name)

        self.client.delete(endpoint)
