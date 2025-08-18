from typing import Literal

from pydantic import AnyHttpUrl, AnyUrl, BaseModel, model_validator

ProxyProtocol = Literal["socks5", "http", "https"]


class SystemProxySettings(BaseModel):
    http_proxy: AnyHttpUrl | None
    https_proxy: AnyHttpUrl | None
    socks5_proxy: AnyUrl | None

    @model_validator(mode="after")
    def validate_minimum_one_proxy(self):
        specified_fields = [
            field
            for field in SystemProxySettings.model_fields
            if self.model_dump()[field] is not None
        ]

        if len(specified_fields) == 0:
            raise ValueError("At least one proxy must be specified")

        return self


class ProxyProfileInput(BaseModel):
    name: str
    is_active: bool
    settings: SystemProxySettings


class ProxyProfile(ProxyProfileInput):
    id: int
