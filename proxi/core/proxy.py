import subprocess
from dataclasses import dataclass
from typing import Literal


@dataclass
class Proxy:
    protocol: Literal["socks5", "http", "https"]
    host: str
    port: int


@dataclass
class ProxyProfile:
    http_proxy: Proxy
    https_proxy: Proxy
    socks5_proxy: Proxy


def get_current_proxy():
    http_proxy_host = subprocess.run(
        ["gsettings", "get", "org.gnome.system.proxy.http", "host"],
        capture_output=True,
        text=True,
    )

    http_proxy_port = subprocess.run(
        ["gsettings", "get", "org.gnome.system.proxy.http", "port"],
        capture_output=True,
        text=True,
    )

    https_proxy_host = subprocess.run(
        ["gsettings", "get", "org.gnome.system.proxy.https", "host"],
        capture_output=True,
        text=True,
    )

    https_proxy_port = subprocess.run(
        ["gsettings", "get", "org.gnome.system.proxy.https", "port"],
        capture_output=True,
        text=True,
    )

    socks_proxy_host = subprocess.run(
        ["gsettings", "get", "org.gnome.system.proxy.socks", "host"],
        capture_output=True,
        text=True,
    )

    socks_proxy_port = subprocess.run(
        ["gsettings", "get", "org.gnome.system.proxy.socks", "port"],
        capture_output=True,
        text=True,
    )

    # TODO: return proxy profile
