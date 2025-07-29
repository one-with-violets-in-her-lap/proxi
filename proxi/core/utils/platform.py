import logging
import os
from enum import Enum

from proxi.core.utils.errors import UnsupportedPlatformError


class Platform(Enum):
    KDE_PLASMA = "KDE Plasma"
    GNOME = "GNOME"
    CINNAMON = "Cinnamon"


_PLATFORMS_BY_DESKTOP_SESSION_VALUE: dict[str, Platform] = {
    "plamsa": Platform.KDE_PLASMA,
    "gnome": Platform.GNOME,
    "cinnamon": Platform.CINNAMON,
}


_logger = logging.getLogger(__name__)


def get_user_platform():
    desktop_session = os.environ.get("DESKTOP_SESSION")

    _logger.info("Checking desktop session: %s", desktop_session)

    if desktop_session not in _PLATFORMS_BY_DESKTOP_SESSION_VALUE:
        raise UnsupportedPlatformError(
            "Your platform/OS is not supported. For now app supports Linux only "
            + f"supports these platforms: {[platform.value for platform in Platform]}"
        )

    detected_platform = _PLATFORMS_BY_DESKTOP_SESSION_VALUE[desktop_session]
    _logger.info("Detected %s", detected_platform.value)
    return detected_platform
