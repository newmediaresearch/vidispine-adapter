from vidispine.typing import BaseJson


class Job:

    def __init__(self, client) -> None:
        self.client = client

    def problem(self) -> BaseJson:
        endpoint = 'job/problem'
        return self.client.get(endpoint)
