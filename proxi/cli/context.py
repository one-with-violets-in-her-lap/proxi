from typing import TypedDict

from proxi.core.proxy_config_clients._base import BaseProxyConfigClient
from proxi.core.services.proxy_profiles import ProxyProfilesService


class CliContext(TypedDict):
    proxy_config: BaseProxyConfigClient
    proxy_profiles_service: ProxyProfilesService
