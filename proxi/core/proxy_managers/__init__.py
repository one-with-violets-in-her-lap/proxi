import logging
from typing import Callable

from proxi.core.models.config import load_config, update_config
from proxi.core.models.proxy import ProxyProfile, SystemProxySettings
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

    def get_proxy_settings(self):
        return self.platform_specific_proxy_manager.get_proxy_settings()

    def set_proxy_settings(self, proxy_settings: SystemProxySettings):
        self.platform_specific_proxy_manager.set_proxy_settings(proxy_settings)

    def get_profiles(self):
        config = load_config()

        proxy_settings = self.get_proxy_settings()

        profiles = config.proxy_profiles.copy()

        profiles = config.proxy_profiles.copy()

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

    def set_active_profile(
        self,
        profile_to_set_active: ProxyProfile,
        do_before_settings_save: Callable[[list[ProxyProfile]], None] | None = None,
    ) -> list[ProxyProfile]:
        """Changes the current active profile and writes changes to the app config

        :param do_before_settings_save: Function `(new_profiles) -> None` that is
            called before updating system proxy settings. Can be for optimistic updates in UIs

        :return: New list of profiles
        """

        _logger.info("Setting profile as active: %s", profile_to_set_active)

        config = load_config()

        for index, profile in enumerate(config.proxy_profiles):
            if profile.is_active:
                profile.is_active = False

            if profile.settings == profile_to_set_active.settings:
                profile.is_active = True
                config.proxy_profiles.pop(index)
                config.proxy_profiles.insert(0, profile)

        if do_before_settings_save is not None:
            do_before_settings_save(config.proxy_profiles)

        self.set_proxy_settings(profile_to_set_active.settings)

        update_config(config)

        return config.proxy_profiles
