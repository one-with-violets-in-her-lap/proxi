from abc import ABC, abstractmethod

from proxi.core.models.proxy import SystemProxySettings


class BaseProxyManager(ABC):
    @abstractmethod
    def get_is_proxy_active(self) -> bool:
        pass

    @abstractmethod
    def set_is_proxy_active(self, is_active: bool):
        pass

    @abstractmethod
    def get_proxy_settings(self) -> SystemProxySettings | None:
        pass

    @abstractmethod
    def set_proxy_settings(self, proxy_settings: SystemProxySettings) -> None:
        pass
