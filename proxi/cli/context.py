from typing import TypedDict

from proxi.core.proxy_config_clients._base import BaseProxyConfigClient


class CliContext(TypedDict):
    proxy_config: BaseProxyConfigClient
