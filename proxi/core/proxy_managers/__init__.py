import logging

from proxi.core.models.config import ProxiAppConfig
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

    def __init__(self, platform: Platform, config: ProxiAppConfig):
        self.platform = platform
        self.platform_specific_proxy_manager = PROXY_MANAGERS_BY_PLATFORM[
            self.platform
        ]()

        self.config = config

    def get_is_proxy_active(self) -> bool:
        return self.platform_specific_proxy_manager.get_is_proxy_active()

    def set_is_proxy_active(self, is_active: bool):
        return self.platform_specific_proxy_manager.set_is_proxy_active(is_active)

    def get_profiles(self):
        proxy_settings = self.platform_specific_proxy_manager.get_proxy_settings()

        profiles = self.config.proxy_profiles.copy()

        profiles = self.config.proxy_profiles.copy()

        profile_matching_with_settings_index: int | None = None
        active_profile_index: int | None = None

        for index, profile in enumerate(profiles):
            if profile.settings == proxy_settings:
                profile_matching_with_settings_index = index

            if profile.is_active:
                active_profile_index = index

        if (
            profile_matching_with_settings_index is not None
            and not profiles[profile_matching_with_settings_index].is_active
        ):
            _logger.warning(
                "System proxy and app mismatch. Current profile is not active. Making it active"
            )

            if active_profile_index is not None:
                profiles[active_profile_index].is_active = False

            profiles[profile_matching_with_settings_index].is_active = True

        if profile_matching_with_settings_index is None and proxy_settings is not None:
            _logger.warning(
                'System proxy and app mismatch. Current profile does not exist. Adding "Unknown" profile'
            )

            if active_profile_index is not None:
                profiles[active_profile_index].is_active = False

            profiles.insert(
                0,
                ProxyProfile(
                    is_active=True, name="Unknown profile", settings=proxy_settings
                ),
            )

        _logger.info("Proxy profiles: %s", profiles)

        return profiles
