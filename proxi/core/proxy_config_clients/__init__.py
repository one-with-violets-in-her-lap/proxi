import logging

from proxi.core.models.proxy import SystemProxySettings
from proxi.core.proxy_config_clients._base import BaseProxyConfigClient
from proxi.core.proxy_config_clients._gnome import GnomeProxyConfig
from proxi.core.proxy_config_clients._kde import KdeProxyConfig
from proxi.core.proxy_config_clients._shell import ShellProxyConfig
from proxi.core.utils.platform import Platform

PROXY_CONFIG_CLIENTS: dict[Platform, list[type[BaseProxyConfigClient]]] = {
    Platform.GNOME: [GnomeProxyConfig, ShellProxyConfig],
    Platform.CINNAMON: [GnomeProxyConfig, ShellProxyConfig],
    Platform.KDE_PLASMA: [KdeProxyConfig, ShellProxyConfig],
}


_logger = logging.getLogger(__name__)


class CrossPlatformProxyConfig(BaseProxyConfigClient):
    """Cross-platform proxy config manager

    Chooses underlying proxy config implementation depending on user platform
    (KDE/GNOME/etc.)
    """

    def __init__(self, platform: Platform):
        self.platform = platform
        self.platform_specific_proxy_configs = [
            config_class() for config_class in PROXY_CONFIG_CLIENTS[self.platform]
        ]

    def get_is_proxy_active(self) -> bool:
        _logger.info(
            "Getting proxy status from %s", self.platform_specific_proxy_configs[0]
        )

        return self.platform_specific_proxy_configs[0].get_is_proxy_active()

    def set_is_proxy_active(self, is_active: bool):
        for config in self.platform_specific_proxy_configs:
            config.set_is_proxy_active(is_active)

    def get_proxy_settings(self):
        _logger.info(
            "Getting proxy settings from %s", self.platform_specific_proxy_configs[0]
        )

        return self.platform_specific_proxy_configs[0].get_proxy_settings()

    def set_proxy_settings(self, proxy_settings: SystemProxySettings):
        for config in self.platform_specific_proxy_configs:
            config.set_proxy_settings(proxy_settings)
