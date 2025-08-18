import timeit

import click

from proxi.cli.context import CliContext


@click.command("on")
@click.pass_context
def handle_proxy_on_command(context: click.Context):
    cli_context: CliContext = context.obj

    start_seconds_time = timeit.default_timer()

    cli_context["proxy_config"].set_is_proxy_active(True)

    milliseconds_took = (timeit.default_timer() - start_seconds_time) * 1000

    click.echo("Proxy is on" + click.style(f" ({milliseconds_took:.1f}ms)", dim=True))


@click.command("off")
@click.pass_context
def handle_proxy_off_command(context: click.Context):
    cli_context: CliContext = context.obj

    start_seconds_time = timeit.default_timer()

    cli_context["proxy_config"].set_is_proxy_active(False)

    milliseconds_took = (timeit.default_timer() - start_seconds_time) * 1000

    click.echo("Proxy is off" + click.style(f" ({milliseconds_took:.1f}ms)", dim=True))
