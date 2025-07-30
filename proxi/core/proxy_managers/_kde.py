import os
import subprocess

from proxi.core.models.proxy import SystemProxySettings
from proxi.core.proxy_managers._base import BaseProxyManager

KDE_CONFIG_PATH = os.path.expanduser("~/.config/kioslaverc")


class KdeProxyManager(BaseProxyManager):
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

    def set_is_proxy_active(self, is_active):
        subprocess.run(
            [
                "kwriteconfig6",
                "--file",
                KDE_CONFIG_PATH,
                "--group",
                "Proxy Settings",
                "--key",
                "ProxyType",
                "1" if is_active else "0",
            ],
        )

    def get_proxy_settings(self):
        http_proxy = self._get_proxy_from_kde_config("httpProxy")
        https_proxy = self._get_proxy_from_kde_config("httpsProxy")
        socks5_proxy = self._get_proxy_from_kde_config("socksProxy")

        return SystemProxySettings(
            http_proxy=http_proxy, https_proxy=https_proxy, socks5_proxy=socks5_proxy
        )

    def set_proxy_settings(self, proxy_settings: SystemProxySettings):
        self._set_proxy_in_kde_config("httpProxy", proxy_settings.http_proxy)
        self._set_proxy_in_kde_config("httpsProxy", proxy_settings.https_proxy)
        self._set_proxy_in_kde_config("socksProxy", proxy_settings.socks5_proxy)

    def _set_proxy_in_kde_config(self, key: str, proxy_url: str | None):
        proxy_config_value = ""

        if proxy_url is not None:
            protocol, host, port = proxy_url.split(":")
            proxy_config_value = f"{protocol}:{host} {port}"

        proxy_update_result = subprocess.run(
            [
                "kwriteconfig6",
                "--file",
                KDE_CONFIG_PATH,
                "--group",
                "Proxy Settings",
                "--key",
                key,
                proxy_config_value,
            ]
        )

        return proxy_update_result

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
