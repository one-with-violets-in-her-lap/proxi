import logging
import os
from enum import Enum

from proxi.core.utils.errors import UnsupportedPlatformError


class Platform(Enum):
    KDE_PLASMA = "KDE Plasma"
    GNOME = "GNOME"


_logger = logging.getLogger(__name__)


def get_user_platform():
    desktop_session = os.environ.get("DESKTOP_SESSION")

    _logger.info("Checking desktop session: %s", desktop_session)

    if desktop_session == "plasma":
        _logger.info("Detected %s", Platform.KDE_PLASMA.value)
        return Platform.KDE_PLASMA
    elif desktop_session == "gnome":
        _logger.info("Detected %s", Platform.GNOME.value)
        return Platform.GNOME
    else:
        raise UnsupportedPlatformError(
            "Your platform/OS is not supported. For now app supports Linux only "
            + f"supports these platforms: {[platform.value for platform in Platform]}"
        )
