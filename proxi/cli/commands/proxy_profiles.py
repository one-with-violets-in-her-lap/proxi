import timeit

import click
from pydantic import ValidationError

from proxi.cli.utils.errors import CliError
from proxi.cli.context import CliContext
from proxi.core.models.proxy import ProxyProfile, ProxyProfileInput
from proxi.core.utils.errors import ProfileAlreadyExistsError

_ERROR_MESSAGES_BY_FIELD_LOC = {
    ("name",): "Profile name is invalid",
    ("settings", "http_proxy"): "HTTP proxy URL is invalid",
    ("settings", "https_proxy"): "HTTPS proxy URL is invalid",
    ("settings", "socks5_proxy"): "SOCKS5 proxy URL is invalid",
    ("settings",): "At least one proxy must be specified",
}


def _format_proxy_profile(profile: ProxyProfile):
    formatted_profile = (
        click.style("● ", fg="green") if profile.is_active else ""
    ) + click.style(profile.name, bold=True)

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

    return formatted_profile + "\n"


@click.group("profiles", invoke_without_command=True)
@click.pass_context
def profiles_commands(
    context: click.Context,
):
    """
    View and manage your profiles
    """

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
        + "\n\n\n"
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
            "+ Profile created"
            + click.style(f"\t({milliseconds_took:.1f} ms)", dim=True)
        )
    except ProfileAlreadyExistsError:
        raise CliError(f'Profile with name "{name}" already exists')
    except ValidationError as error:
        first_error = error.errors()[0]

        raise CliError(
            _ERROR_MESSAGES_BY_FIELD_LOC.get(first_error["loc"]) or first_error["msg"]
        )


@profiles_commands.command("update", help="Update a proxy profile")
@click.argument("name", required=True)
@click.option("--name", "new_name")
@click.option("--http", "http_proxy")
@click.option("--https", "https_proxy")
@click.option("--socks5", "socks5_proxy")
@click.pass_context
def _handle_update_profile_command(
    context: click.Context,
    name: str,
    new_name: str | None,
    http_proxy: str | None,
    https_proxy: str | None,
    socks5_proxy: str | None,
):
    start_seconds_time = timeit.default_timer()

    cli_context: CliContext = context.obj

    matching_profiles = [
        profile
        for profile in cli_context["proxy_profiles_service"].get_profiles()
        if profile.name == name
    ]

    if len(matching_profiles) == 0:
        raise CliError(f'Profile with name "{name}" does not exist')

    target_profile = matching_profiles[0]

    try:
        profile_update_input = {
            "name": new_name if new_name is not None else name,
            "is_active": False,
            "settings": {
                "http_proxy": http_proxy,
                "https_proxy": https_proxy,
                "socks5_proxy": socks5_proxy,
            },
        }

        if http_proxy is None:
            profile_update_input["settings"]["http_proxy"] = (
                target_profile.settings.http_proxy
            )

        if https_proxy is None:
            profile_update_input["settings"]["https_proxy"] = (
                target_profile.settings.https_proxy
            )

        if socks5_proxy is None:
            profile_update_input["settings"]["socks5_proxy"] = (
                target_profile.settings.socks5_proxy
            )

        cli_context["proxy_profiles_service"].update_profile(
            matching_profiles[0].id,
            ProxyProfileInput.model_validate(profile_update_input),
        )

        milliseconds_took = (timeit.default_timer() - start_seconds_time) * 1000

        click.echo(
            click.style("+", fg="green", dim=True)
            + "Profile updated"
            + click.style(f"\t({milliseconds_took:.1f} ms)", dim=True)
        )
    except ProfileAlreadyExistsError:
        raise CliError(f'Profile with name "{name}" already exists')
    except ValidationError as error:
        first_error = error.errors()[0]

        raise CliError(
            _ERROR_MESSAGES_BY_FIELD_LOC.get(first_error["loc"]) or first_error["msg"]
        )


@profiles_commands.command("delete")
@click.pass_context
@click.argument("name", required=True)
def _handle_profile_delete_command(context: click.Context, name: str):
    start_seconds_time = timeit.default_timer()

    cli_context: CliContext = context.obj

    profiles = cli_context["proxy_profiles_service"].get_profiles()
    profiles_to_delete = [profile for profile in profiles if profile.name == name]

    if len(profiles_to_delete) == 0:
        raise CliError(f"Profile with name {name} cannot be found")

    cli_context["proxy_profiles_service"].delete_profile(profiles_to_delete[0].id)

    milliseconds_took = (timeit.default_timer() - start_seconds_time) * 1000

    click.echo(
        click.style("-", fg="red")
        + " Profile deleted"
        + click.style(f"\t({milliseconds_took:.1f} ms)", dim=True)
    )


@click.command("activate")
@click.pass_context
@click.argument("profile_name", required=True)
def handle_profile_activate_command(context: click.Context, profile_name: str):
    """Select profile which proxy settings to use"""

    start_seconds_time = timeit.default_timer()

    cli_context: CliContext = context.obj

    profiles = cli_context["proxy_profiles_service"].get_profiles()
    profiles_to_delete = [
        profile for profile in profiles if profile.name == profile_name
    ]

    if len(profiles_to_delete) == 0:
        raise CliError(f"Profile with name {profile_name} cannot be found")

    cli_context["proxy_profiles_service"].set_profile_as_active(
        profiles_to_delete[0].id
    )

    milliseconds_took = (timeit.default_timer() - start_seconds_time) * 1000

    click.echo(
        click.style("🗸", fg="green", dim=True)
        + " Profile activated"
        + click.style(f"\t({milliseconds_took:.1f} ms)", dim=True)
    )
