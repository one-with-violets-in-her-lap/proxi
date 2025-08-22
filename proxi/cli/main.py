import click

from proxi.cli.ascii_art import ASCII_ART
from proxi.cli.commands import commands
from proxi.cli.context import CliContext
from proxi.core.models.config import ProxiAppConfigProvider
from proxi.core.proxy_config_clients import CrossPlatformProxyConfig
from proxi.core.services.proxy_profiles import ProxyProfilesService
from proxi.core.utils.platform import get_user_settings_platform


@click.group(help=ASCII_ART)
@click.pass_context
def cli(context: click.Context):
    proxy_config = CrossPlatformProxyConfig(get_user_settings_platform())

    context_obj: CliContext = {
        "proxy_config": proxy_config,
        "proxy_profiles_service": ProxyProfilesService(
            ProxiAppConfigProvider(), proxy_config
        ),
    }
    context.obj = context_obj


for command in commands:
    cli.add_command(command)

if __name__ == "__main__":
    cli()
