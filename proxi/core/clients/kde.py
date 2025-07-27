import os
import subprocess

from proxi.core.proxy import ProxyProfile

KDE_CONFIG_PATH = os.path.expanduser("~/.config/kioslaverc")


class KdeProxyClient:
    def get_is_proxy_active(self):
        proxy_type = (
            subprocess.check_output(
                [
                    "kreadconfig6",
                    "--file",
                    KDE_CONFIG_PATH,
                    "--group",
                    "Proxy Settings",
                    "--key",
                    "ProxyType",
                ],
            )
            .decode()
            .strip()
        )

        return proxy_type == "1"

    def get_current_proxy_profile(self):
        http_proxy = self._get_proxy_from_kde_config("httpProxy")
        https_proxy = self._get_proxy_from_kde_config("httpsProxy")
        socks5_proxy = self._get_proxy_from_kde_config("socksProxy")

        return ProxyProfile(
            http_proxy=http_proxy, https_proxy=https_proxy, socks5_proxy=socks5_proxy
        )

    def _get_proxy_from_kde_config(self, key: str):
        proxy = (
            subprocess.check_output(
                [
                    "kreadconfig6",
                    "--file",
                    KDE_CONFIG_PATH,
                    "--group",
                    "Proxy Settings",
                    "--key",
                    key,
                ],
            )
            .decode()
            .strip()
        )

        if proxy == "":
            return None

        host, port = proxy.split(" ")

        return host + ":" + port
