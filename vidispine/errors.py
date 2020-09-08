

class ConfigError(Exception):
    pass


class APIError(Exception):
    pass


class NotFound(APIError):
    pass
