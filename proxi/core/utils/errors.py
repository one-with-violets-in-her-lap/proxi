class ProxiAppError(Exception):
    pass


class UnsupportedPlatformError(ProxiAppError):
    pass


class ProfileAlreadyExistsError(ProxiAppError):
    def __init__(self):
        super().__init__("Profile with the same name already exists")


class NotFoundError(ProxiAppError):
    pass
