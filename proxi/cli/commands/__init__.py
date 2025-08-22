from proxi.cli.commands.proxy_profiles import (
    handle_profile_activate_command,
    profiles_commands,
)
from proxi.cli.commands.proxy_switch import (
    handle_proxy_off_command,
    handle_proxy_on_command,
    handle_proxy_status_command,
)

commands = [
    handle_proxy_status_command,
    handle_proxy_on_command,
    handle_proxy_off_command,
    profiles_commands,
    handle_profile_activate_command,
]
