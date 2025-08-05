from typing import Literal

from pydantic import AnyHttpUrl, AnyUrl, BaseModel

ProxyProtocol = Literal["socks5", "http", "https"]


class SystemProxySettings(BaseModel):
    http_proxy: AnyHttpUrl | None
    https_proxy: AnyHttpUrl | None
    socks5_proxy: AnyUrl | None


class ProxyProfile(BaseModel):
    name: str
    is_active: bool
    settings: SystemProxySettings
