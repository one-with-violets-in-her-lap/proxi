import logging

from proxi.core.models.proxy import ProxyProfile
from proxi.core.proxy_managers._base import BaseProxyManager
from proxi.core.proxy_managers._gnome import GnomeProxyManager
from proxi.core.proxy_managers._kde import KdeProxyManager
from proxi.core.utils.platform import Platform

PROXY_MANAGERS_BY_PLATFORM: dict[Platform, type[BaseProxyManager]] = {
    Platform.GNOME: GnomeProxyManager,
    Platform.CINNAMON: GnomeProxyManager,
    Platform.KDE_PLASMA: KdeProxyManager,
}


_logger = logging.getLogger(__name__)


class ProxyManager:
    """Cross-platform proxy manager

    Chooses underlying proxy manager implementation depending on user platform
    (KDE/GNOME/etc.)
    """

    def __init__(self, platform: Platform):
        self.platform = platform
        self.platform_specific_proxy_manager = PROXY_MANAGERS_BY_PLATFORM[
            self.platform
        ]()

    def get_is_proxy_active(self) -> bool:
        return self.platform_specific_proxy_manager.get_is_proxy_active()

    def set_is_proxy_active(self, is_active: bool):
        return self.platform_specific_proxy_manager.set_is_proxy_active(is_active)

    def get_profiles(self):
        proxy_settings = self.platform_specific_proxy_manager.get_proxy_settings()

        if proxy_settings is None:
            return []

        profiles = [
            ProxyProfile(name="Unknown profie", is_active=True, settings=proxy_settings)
        ]

        _logger.info("Proxy profiles: %s", profiles)

        return profiles
