from dataclasses import dataclass
from typing import Literal

ProxyProtocol = Literal["socks5", "http", "https"]


@dataclass
class SystemProxySettings:
    http_proxy: str | None
    https_proxy: str | None
    socks5_proxy: str | None
