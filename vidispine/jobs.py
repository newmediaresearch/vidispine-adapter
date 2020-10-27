from vidispine.base import EntityBase
from vidispine.typing import BaseJson


class Job(EntityBase):

    entity = 'job'

    def __init__(self, client) -> None:
        self.client = client

    def get(self, job_id: str) -> BaseJson:
        endpoint = self._build_url(job_id)
        return self.client.get(endpoint)

    def list_problems(self) -> BaseJson:
        endpoint = self._build_url('problem')
        return self.client.get(endpoint)
