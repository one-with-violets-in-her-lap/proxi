import timeit

import click
from pydantic import ValidationError

from proxi.cli.commands.utils.errors import CliError
from proxi.cli.context import CliContext
from proxi.core.models.proxy import ProxyProfile, ProxyProfileInput

_ERROR_MESSAGES_BY_FIELD_LOC = {
    ("name",): "Profile name is invalid",
    ("settings", "http_proxy"): "HTTP proxy URL is invalid",
    ("settings", "https_proxy"): "HTTPS proxy URL is invalid",
    ("settings", "socks5_proxy"): "SOCKS5 proxy URL is invalid",
    ("settings",): "At least one proxy must be specified",
}


def _format_proxy_profile(profile: ProxyProfile):
    DIVIDER = click.style("----------------------------", dim=True)

    formatted_profile = (
        DIVIDER
        + "\n"
        + click.style(profile.name, bold=True)
        + click.style(f" ({profile.id})", dim=True)
        + "\n"
    )

    if profile.settings.http_proxy is not None:
        formatted_profile = formatted_profile + f"\nHTTP: {profile.settings.http_proxy}"

    if profile.settings.https_proxy is not None:
        formatted_profile = (
            formatted_profile + f"\nHTTPS: {profile.settings.https_proxy}"
        )

    if profile.settings.socks5_proxy is not None:
        formatted_profile = (
            formatted_profile + f"\nSOCKS5: {profile.settings.socks5_proxy}"
        )

    return formatted_profile + "\n" + DIVIDER


@click.group("profiles", invoke_without_command=True)
@click.pass_context
def profiles_commands(
    context: click.Context,
):
    if context.invoked_subcommand is not None:
        return

    start_seconds_time = timeit.default_timer()

    cli_context: CliContext = context.obj

    proxy_profile_list = cli_context["proxy_profiles_service"].get_profiles()

    formatted_proxy_profiles = [
        _format_proxy_profile(profile) for profile in proxy_profile_list
    ]

    milliseconds_took = (timeit.default_timer() - start_seconds_time) * 1000

    click.echo(
        click.style("\n* Proxi / profiles", bold=True)
        + "\n\n"
        + "\n\n".join(formatted_proxy_profiles)
        + click.style(f"\n\n\t\t({milliseconds_took:.1f} ms)", dim=True)
    )


@profiles_commands.command("create", help="Create a proxy profile")
@click.argument("name", required=True)
@click.option("--http", "http_proxy")
@click.option("--https", "https_proxy")
@click.option("--socks5", "socks5_proxy")
@click.pass_context
def _handle_create_profile_command(
    context: click.Context,
    name: str,
    http_proxy: str | None,
    https_proxy: str | None,
    socks5_proxy: str | None,
):
    start_seconds_time = timeit.default_timer()

    cli_context: CliContext = context.obj

    try:
        proxy_profile = ProxyProfileInput.model_validate(
            {
                "name": name,
                "is_active": False,
                "settings": {
                    "http_proxy": http_proxy,
                    "https_proxy": https_proxy,
                    "socks5_proxy": socks5_proxy,
                },
            }
        )

        cli_context["proxy_profiles_service"].add_profile(proxy_profile)

        milliseconds_took = (timeit.default_timer() - start_seconds_time) * 1000

        click.echo(
            "+ Profile created     "
            + click.style(f"({milliseconds_took:.1f} ms)", dim=True)
        )
    except ValidationError as error:
        first_error = error.errors()[0]

        raise CliError(
            _ERROR_MESSAGES_BY_FIELD_LOC.get(first_error["loc"]) or first_error["msg"]
        )


@profiles_commands.command("delete")
@click.argument("profile_id", required=True, type=click.INT)
def _handle_profile_delete_command(context: click.Context, profile_id: int):
    try:
        cli_context: CliContext = context.obj

        cli_context["proxy_profiles_service"].delete_profile(profile_id)
    except:
        pass
