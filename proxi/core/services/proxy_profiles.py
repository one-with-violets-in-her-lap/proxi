from proxi.core.models.config import ProxiAppConfigProvider
from proxi.core.models.proxy import ProxyProfile, ProxyProfileInput
from proxi.core.proxy_config_clients._base import BaseProxyConfigClient
from proxi.core.utils.errors import NotFoundError, ProfileAlreadyExistsError


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

    def add_profile(self, new_profile: ProxyProfileInput):
        config = self.app_config.get_or_load_config()

        same_name_profiles = [
            profile
            for profile in config.proxy_profiles
            if profile.name == new_profile.name
        ]

        if len(same_name_profiles) > 0:
            raise ProfileAlreadyExistsError()

        last_profile_id = (
            config.proxy_profiles[-1].id if len(config.proxy_profiles) > 0 else 0
        )

        config.proxy_profiles.append(
            ProxyProfile.model_validate(
                {**new_profile.model_dump(), "id": last_profile_id + 1}
            )
        )

        self.app_config.update_config(config)

    def set_profile_as_active(self, profile_id: int):
        config = self.app_config.get_or_load_config()

        new_active_profile: ProxyProfile | None = None

        for index, profile in enumerate(config.proxy_profiles):
            if profile.id == profile_id:
                profile.is_active = True

                config.proxy_profiles.pop(index)
                config.proxy_profiles.insert(0, profile)

                new_active_profile = profile
            else:
                profile.is_active = False

        if new_active_profile is None:
            raise NotFoundError()

        self.app_config.update_config(config)

        self.proxy_config_client.set_proxy_settings(new_active_profile.settings)

    def delete_profile(self, profile_id: int):
        config = self.app_config.get_or_load_config()

        indices_to_delete = [
            index
            for index, profile in enumerate(config.proxy_profiles)
            if profile.id == profile_id
        ]

        if len(indices_to_delete) == 0:
            raise NotFoundError(f"Profile with id {profile_id} cannot be found")

        config.proxy_profiles.pop(indices_to_delete[0])

        self.app_config.update_config(config)

    def update_profile(self, target_profile_id: int, new_profile: ProxyProfileInput):
        config = self.app_config.get_or_load_config()

        for index, profile in enumerate(config.proxy_profiles):
            if profile.name == new_profile.name and profile.id != target_profile_id:
                raise ProfileAlreadyExistsError()

            if profile.id == target_profile_id:
                config.proxy_profiles[index] = ProxyProfile(
                    id=target_profile_id, **new_profile.model_dump()
                )

        self.app_config.update_config(config)
