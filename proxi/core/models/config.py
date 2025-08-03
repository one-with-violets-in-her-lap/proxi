import logging
import os

from pydantic import BaseModel

from proxi.core.models.proxy import ProxyProfile


class ProxiAppConfig(BaseModel):
    proxy_profiles: list[ProxyProfile]


_DEFAULT_CONFIG = ProxiAppConfig(proxy_profiles=[])


_logger = logging.getLogger(__name__)


class ProxiAppConfigProvider:
    def __init__(self, config_path=os.path.expanduser("~/.config/proxi.json")):
        self._config: ProxiAppConfig | None = None
        self.config_path = config_path

    def get_or_load_config(self):
        """
        If config was already loaded, returns the up-to-date in-memory version of
        it. Otherwise, loads the config from the filesystem
        """

        if self._config is not None:
            return self._config

        if not os.path.exists(self.config_path):
            _logger.info(
                "Config file does not exist at %s. Creating a new one", self.config_path
            )

            with open(self.config_path, "wt") as config_stream:
                config_stream.write(_DEFAULT_CONFIG.model_dump_json())

            return _DEFAULT_CONFIG

        with open(self.config_path, "rt") as config_stream:
            return ProxiAppConfig.model_validate_json(config_stream.read())

    def update_config(
        self,
        new_config: ProxiAppConfig,
    ):
        self._config = new_config

        with open(self.config_path, "wt") as config_stream:
            config_stream.write(new_config.model_dump_json())
