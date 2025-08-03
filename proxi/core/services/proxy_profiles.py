from proxi.core.models.config import ProxiAppConfigProvider
from proxi.core.models.proxy import ProxyProfile
from proxi.core.proxy_config_clients._base import BaseProxyConfigClient
from proxi.core.utils.errors import ProfileAlreadyExistsError


class ProxyProfilesService:
    def __init__(
        self,
        app_config: ProxiAppConfigProvider,
        proxy_config_client: BaseProxyConfigClient,
    ):
        self.app_config = app_config
        self.proxy_config_client = proxy_config_client

    # def update_profiles_config(self):
    #     """Updates the profile list based on system proxy settings and writes changes to the app config
    #
    #     - Adds an "Unknown" profile when current system proxy settings don't match to any
    #       of existing profiles
    #     - Finds the currently active profile based on system proxy settings. If it's not active
    #       in the app config, it updates it
    #     """
    #
    #     config = self.app_config.get_or_load_config()
    #
    #     proxy_settings = self.proxy_config_client.get_proxy_settings()

    def get_profiles(self):
        return self.app_config.get_or_load_config().proxy_profiles

    def add_profile(self, new_profile: ProxyProfile):
        config = self.app_config.get_or_load_config()

        same_profiles = [
            profile
            for profile in config.proxy_profiles
            if profile.name == new_profile.name
            or profile.settings == new_profile.settings
        ]

        if len(same_profiles) > 0:
            raise ProfileAlreadyExistsError()

        config.proxy_profiles.append(new_profile)

        self.app_config.update_config(config)

    def set_profile_as_active(self, profile_to_set_active: ProxyProfile):
        config = self.app_config.get_or_load_config()

        for index, profile in enumerate(config.proxy_profiles):
            if profile.name == profile_to_set_active.name:
                profile.is_active = True

                config.proxy_profiles.pop(index)
                config.proxy_profiles.insert(0, profile)
            else:
                profile.is_active = False

        self.app_config.update_config(config)
        self.proxy_config_client.set_proxy_settings(profile_to_set_active.settings)

    def delete_profile(self, profile_to_delete: ProxyProfile):
        config = self.app_config.get_or_load_config()

        for index, profile in enumerate(config.proxy_profiles):
            if profile.name == profile_to_delete.name:
                config.proxy_profiles.pop(index)

        self.app_config.update_config(config)
