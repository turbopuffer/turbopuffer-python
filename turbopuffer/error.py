class TurbopufferError(Exception):
    pass


class AuthenticationError(TurbopufferError):
    pass


class APIError(TurbopufferError):
    def __init__(self, status_code: int, status_name: str, message: str):
        self.status_code = status_code
        self.status_name = status_name
        super().__init__(f'{status_name} (HTTP {status_code}): {message}')

class NotFoundError(APIError):
    pass

def raise_api_error(status_code, status_name, message):
    if status_code == 404:
        raise NotFoundError(status_code, status_name, message)
    else:
        raise APIError(status_code, status_name, message)
