"""Module for managing script that runs on shell startup (shell profile)

Can be useful for persisting environment variables
"""

import logging
import os

_logger = logging.getLogger(__name__)


def update_app_shell_profile(setup_file_path: str, startup_script: str):
    with open(setup_file_path, "wt") as setup_file_stream:
        setup_file_stream.write(startup_script)

    generic_shell_profile_file_path = os.path.expanduser("~/.profile")
    bash_profile_file_path = os.path.expanduser("~/.bash_profile")

    profile_file_to_use = generic_shell_profile_file_path

    if os.path.exists(bash_profile_file_path):
        _logger.info(
            "~/.bash_profile file exists, choosing it over generic ~/.profile file"
        )
        profile_file_to_use = bash_profile_file_path

    home_path = os.path.expanduser("~")

    setup_file_path_with_home_variable = setup_file_path.replace(home_path, "$HOME")

    setup_script_import = f'. "{setup_file_path_with_home_variable}'

    _logger.debug(
        "Adding this line to %s : %s", profile_file_to_use, setup_script_import
    )

    with (
        open(profile_file_to_use, "rt") as profile_file_read_stream,
    ):
        shell_profile_content = profile_file_read_stream.read()

        if setup_script_import in shell_profile_content:
            _logger.info("Setup script is already imported in shell profile")
            return

        with open(profile_file_to_use, "wt") as profile_file_write_stream:
            profile_file_write_stream.write(
                shell_profile_content
                + "\n\n"
                + "# Proxi app support for shell\n"
                + setup_script_import
            )
