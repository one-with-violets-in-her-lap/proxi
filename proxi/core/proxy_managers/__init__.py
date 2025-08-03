import logging
from typing import Callable

from proxi.core.models.config import ProxiAppConfig, ProxiAppConfigProvider
from proxi.core.models.proxy import ProxyProfile, SystemProxySettings
from proxi.core.proxy_managers._base import BaseProxyManager
from proxi.core.proxy_managers._gnome import GnomeProxyManager
from proxi.core.proxy_managers._kde import KdeProxyManager
from proxi.core.utils.errors import ProfileNameAlreadyExistsError
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

    def __init__(self, platform: Platform, config: ProxiAppConfigProvider):
        self.config_provider = config

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

    def get_profiles(
        self,
        config: ProxiAppConfig | None = None,
        proxy_settings: SystemProxySettings | None = None,
    ):
        """Gets profiles from app config and matches them with system settings, determining the active profile

        If the current system proxy settings can't be matched to any existing profile, creates an
        "Unknown" profile

        :param config: Lets you specify a config that the method will use instead
            of loading it by itself
        :param proxy_settings: Lets you specify a settings that the method will match
            profile to instead of loading them by itself
        """

        config = self.config_provider.get_or_load_config() if config is None else config

        proxy_settings = (
            self.get_proxy_settings() if proxy_settings is None else proxy_settings
        )

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

        config = self.config_provider.get_or_load_config()

        for index, profile in enumerate(config.proxy_profiles):
            if profile.is_active:
                profile.is_active = False

            if profile.settings == profile_to_set_active.settings:
                profile.is_active = True
                config.proxy_profiles.pop(index)
                config.proxy_profiles.insert(0, profile)

        new_profiles = self.get_profiles(config, profile_to_set_active.settings)

        if do_before_settings_save is not None:
            do_before_settings_save(new_profiles)

        self.set_proxy_settings(profile_to_set_active.settings)

        self.config_provider.update_config(config)

        return new_profiles

    def add_profile(self, profile_to_add: ProxyProfile):
        """Adds a new profile to the app config

        :return: New list of profiles
        """

        config = self.config_provider.get_or_load_config()

        profiles_with_same_name = [
            profile
            for profile in config.proxy_profiles
            if profile.name == profile_to_add.name
        ]

        if len(profiles_with_same_name) > 0:
            raise ProfileNameAlreadyExistsError(profile_to_add.name)

        config.proxy_profiles.append(profile_to_add)

        self.config_provider.update_config(config)
