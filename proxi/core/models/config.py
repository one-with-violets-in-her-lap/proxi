import logging
import os

from pydantic import BaseModel

from proxi.core.models.proxy import ProxyProfile


class ProxiAppConfig(BaseModel):
    proxy_profiles: list[ProxyProfile]


_DEFAULT_CONFIG = ProxiAppConfig(proxy_profiles=[])


_logger = logging.getLogger(__name__)


def load_config(config_path: str = os.path.expanduser("~/.config/proxi.json")):
    if not os.path.exists(config_path):
        _logger.info(
            "Config file does not exist at %s. Creating a new one", config_path
        )

        with open(config_path, "wt") as config_stream:
            config_stream.write(_DEFAULT_CONFIG.model_dump_json())

        return _DEFAULT_CONFIG

    with open(config_path, "rt") as config_stream:
        return ProxiAppConfig.model_validate_json(config_stream.read())


def update_config(
    new_config: ProxiAppConfig,
    config_path: str = os.path.expanduser("~/.config/proxi.json"),
):
    with open(config_path, "wt") as config_stream:
        config_stream.write(new_config.model_dump_json())
