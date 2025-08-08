import logging
import shutil
from enum import Enum


class SettingsPlatform(Enum):
    GSETTINGS = "GSETTINGS"
    KDE_6_CONFIG = "KDE_6_CONFIG"
    SHELL_ENVIRONMENT = "SHELL"


_logger = logging.getLogger(__name__)


def get_user_settings_platform():
    kreadconfig6_path = shutil.which("kreadconfig6")

    if kreadconfig6_path is not None:
        _logger.info("KDE 6 config tool detected")
        return SettingsPlatform.KDE_6_CONFIG

    gsettings_bin_path = shutil.which("gsettings")

    if gsettings_bin_path is not None:
        _logger.info("GSettings tool detected")
        return SettingsPlatform.GSETTINGS

    _logger.info(
        "No support settings utility found, falling back to basic shell environment variables"
    )
    return SettingsPlatform.SHELL_ENVIRONMENT
