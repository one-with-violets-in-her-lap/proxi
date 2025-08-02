class ProxiAppError(Exception):
    pass


class UnsupportedPlatformError(ProxiAppError):
    pass


class ProfileNameAlreadyExistsError(ProxiAppError):
    def __init__(self, name: str):
        super().__init__(
            f'Profile with name "{name}" already exists. The name must be unique'
        )
