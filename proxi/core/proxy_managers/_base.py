from abc import ABC, abstractmethod

from proxi.core.proxy import ProxyProfile


class BaseProxyManager(ABC):
    @abstractmethod
    def get_is_proxy_active(self) -> bool:
        pass

    @abstractmethod
    def set_is_proxy_active(self, is_active: bool):
        pass

    @abstractmethod
    def get_current_proxy_profile(self) -> ProxyProfile | None:
        pass

    @abstractmethod
    def set_proxy_profile(self, proxy_profile: ProxyProfile) -> None:
        pass
