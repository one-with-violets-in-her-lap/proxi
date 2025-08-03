import logging

from proxi.core.models.proxy import SystemProxySettings
from proxi.core.proxy_config_clients._base import BaseProxyConfigClient
from proxi.core.proxy_config_clients._gnome import GnomeProxyConfig
from proxi.core.proxy_config_clients._kde import KdeProxyConfig
from proxi.core.utils.platform import Platform

PROXY_CONFIG_CLIENTS: dict[Platform, type[BaseProxyConfigClient]] = {
    Platform.GNOME: GnomeProxyConfig,
    Platform.CINNAMON: GnomeProxyConfig,
    Platform.KDE_PLASMA: KdeProxyConfig,
}


_logger = logging.getLogger(__name__)


class CrossPlatformProxyConfig(BaseProxyConfigClient):
    """Cross-platform proxy config manager

    Chooses underlying proxy config implementation depending on user platform
    (KDE/GNOME/etc.)
    """

    def __init__(self, platform: Platform):
        self.platform = platform
        self.platform_specific_proxy_manager = PROXY_CONFIG_CLIENTS[self.platform]()

    def get_is_proxy_active(self) -> bool:
        return self.platform_specific_proxy_manager.get_is_proxy_active()

    def set_is_proxy_active(self, is_active: bool):
        return self.platform_specific_proxy_manager.set_is_proxy_active(is_active)

    def get_proxy_settings(self):
        return self.platform_specific_proxy_manager.get_proxy_settings()

    def set_proxy_settings(self, proxy_settings: SystemProxySettings):
        self.platform_specific_proxy_manager.set_proxy_settings(proxy_settings)
