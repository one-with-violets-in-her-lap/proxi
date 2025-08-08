import logging
import subprocess
import urllib.parse

from proxi.core.models.proxy import ProxyProtocol, SystemProxySettings
from proxi.core.proxy_config_clients._base import BaseProxyConfigClient

_PROXY_TYPES_BY_PROTOCOL: dict[ProxyProtocol, str] = {
    "http": "http",
    "https": "https",
    "socks5": "socks",
}

_logger = logging.getLogger(__name__)


class GSettingsProxyConfig(BaseProxyConfigClient):
    """
    Proxy config implementation for systems with
    [gsettings](http://www.linux-commands-examples.com/gsettings) utility (commonly GNOME)
    """

    def get_is_proxy_active(self):
        return self._get_gsettings_value("org.gnome.system.proxy", "mode") == "manual"

    def set_is_proxy_active(self, is_active: bool):
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.gnome.system.proxy",
                "mode",
                "manual" if is_active else "none",
            ]
        )

    def get_proxy_settings(self):
        return SystemProxySettings.model_validate(
            dict(
                http_proxy=self._get_proxy_from_gsettings("http"),
                https_proxy=self._get_proxy_from_gsettings("https"),
                socks5_proxy=self._get_proxy_from_gsettings("socks5"),
            )
        )

    def set_proxy_settings(self, proxy_settings):
        self._set_proxy_in_gsettings(str(proxy_settings.http_proxy), "http")
        self._set_proxy_in_gsettings(str(proxy_settings.https_proxy), "https")
        self._set_proxy_in_gsettings(str(proxy_settings.socks5_proxy), "socks5")

    def _get_proxy_from_gsettings(self, protocol: ProxyProtocol):
        gnome_proxy_type = _PROXY_TYPES_BY_PROTOCOL[protocol]

        host = self._get_gsettings_value(
            f"org.gnome.system.proxy.{gnome_proxy_type}", "host"
        )
        port = self._get_gsettings_value(
            f"org.gnome.system.proxy.{gnome_proxy_type}", "port"
        )

        if host == "":
            _logger.info(
                "Cannot find %s proxy because the host setting is empty", protocol
            )
            return None

        return f"{protocol}://{host}:{port}"

    def _get_gsettings_value(self, setting_path: str, key: str):
        return (
            subprocess.check_output(["gsettings", "get", setting_path, key])
            .decode()
            .strip()
            .replace("'", "")
        )

    def _set_proxy_in_gsettings(self, proxy_url: str | None, protocol: ProxyProtocol):
        gnome_proxy_type = _PROXY_TYPES_BY_PROTOCOL[protocol]

        proxy_host = ""
        proxy_port = ""

        if proxy_url is not None:
            parsed_url = urllib.parse.urlparse(proxy_url)
            netloc_parts = parsed_url.netloc.rpartition(":")
            proxy_host = netloc_parts[0]
            proxy_port = netloc_parts[-1]

        proxy_host_update_result = subprocess.run(
            [
                "gsettings",
                "set",
                f"org.gnome.system.proxy.{gnome_proxy_type}",
                "host",
                proxy_host,
            ]
        )

        proxy_port_update_result = subprocess.run(
            [
                "gsettings",
                "set",
                f"org.gnome.system.proxy.{gnome_proxy_type}",
                "port",
                "0" if proxy_port == "" else str(proxy_port),
            ]
        )

        return proxy_host_update_result, proxy_port_update_result
