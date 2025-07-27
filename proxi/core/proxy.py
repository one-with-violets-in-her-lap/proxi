import subprocess
from dataclasses import dataclass


@dataclass
class ProxyProfile:
    http_proxy_url: str | None
    https_proxy_url: str | None
    socks_proxy_url: str | None


def get_current_proxy() -> ProxyProfile:
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

    return ProxyProfile(
        http_proxy_url=f"{http_proxy_host}:{http_proxy_port}",
        https_proxy_url=f"{https_proxy_host}:{https_proxy_port}",
        socks_proxy_url=f"{socks_proxy_host}:{socks_proxy_port}",
    )
