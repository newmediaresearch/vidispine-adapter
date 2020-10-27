from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class MetadataFieldGroup(EntityBase):

    entity = 'metadata-field/field-group'

    def get(self, field_group_name: str, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = self._build_url(field_group_name)

        return self.client.get(endpoint, params=params)

    def create(self, field_group_name: str, params: dict = None) -> None:
        if params is None:
            params = {}

        endpoint = self._build_url(field_group_name)

        self.client.put(endpoint, params=params)

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        return self.client.get(self.entity, params=params)

    def add_field_to_group(
        self,
        field_group_name: str,
        field_name: str
    ) -> None:

        endpoint = self._build_url(f'{field_group_name}/{field_name}')
        self.client.put(endpoint)

    def remove_field_from_group(
        self,
        field_group_name: str,
        field_name: str
    ) -> None:

        endpoint = self._build_url(f'{field_group_name}/{field_name}')
        self.client.delete(endpoint)

    def add_group_to_group(
        self,
        parent_group_name: str,
        child_group_name: str
    ) -> None:

        endpoint = self._build_url(
            f'{parent_group_name}/group/{child_group_name}'
        )
        self.client.put(endpoint)

    def delete(self, field_group_name: str) -> None:
        endpoint = self._build_url(field_group_name)
        self.client.delete(endpoint)

    def remove_group_from_group(
        self,
        parent_group_name: str,
        child_group_name: str
    ) -> None:

        endpoint = self._build_url(
            f'{parent_group_name}/group/{child_group_name}'
        )
        self.client.delete(endpoint)


class MetadataField(EntityBase):

    entity = 'metadata-field'

    def create(self, metadata: dict, field_name: str) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = self._build_url(field_name)

        return self.client.put(endpoint, json=metadata)

    def update(self, metadata: dict, field_name: str) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = self._build_url(field_name)

        return self.client.put(endpoint, json=metadata)

    def get(
            self,
            field_name: str,
            params: dict = {}
    ) -> BaseJson:
        if not field_name:
            raise InvalidInput("Please supply a field name")

        endpoint = self._build_url(field_name)

        return self.client.get(endpoint, params=params)

    def list(self):
        return self.client.get(self.entity)

    def delete(self, field_name: str) -> None:
        endpoint = self._build_url(field_name)
        self.client.delete(endpoint)
