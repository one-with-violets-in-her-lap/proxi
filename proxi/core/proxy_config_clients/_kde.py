import os
import subprocess

from proxi.core.utils.url_parsing import get_origin_and_port
from proxi.core.models.proxy import SystemProxySettings
from proxi.core.proxy_config_clients._base import BaseProxyConfigClient

KDE_CONFIG_PATH = os.path.expanduser("~/.config/kioslaverc")


class KdeProxyConfig(BaseProxyConfigClient):
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

        return SystemProxySettings.model_validate(
            dict(
                http_proxy=http_proxy,
                https_proxy=https_proxy,
                socks5_proxy=socks5_proxy,
            )
        )

    def set_proxy_settings(self, proxy_settings: SystemProxySettings):
        self._set_proxy_in_kde_config("httpProxy", str(proxy_settings.http_proxy))
        self._set_proxy_in_kde_config("httpsProxy", str(proxy_settings.https_proxy))
        self._set_proxy_in_kde_config("socksProxy", str(proxy_settings.socks5_proxy))

    def _set_proxy_in_kde_config(self, key: str, proxy_url: str | None):
        proxy_config_value = ""

        if proxy_url is not None:
            origin, port = get_origin_and_port(proxy_url)
            proxy_config_value = f"{origin} {port}"

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
