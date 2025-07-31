from typing import Literal

from pydantic import BaseModel

ProxyProtocol = Literal["socks5", "http", "https"]


class SystemProxySettings(BaseModel):
    http_proxy: str | None
    https_proxy: str | None
    socks5_proxy: str | None


class ProxyProfile(BaseModel):
    name: str
    is_active: bool
    settings: SystemProxySettings
