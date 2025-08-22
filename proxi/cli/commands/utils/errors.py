import click

from proxi.core.utils.errors import ProxiAppError


class CliError(click.ClickException, ProxiAppError):
    def format_message(self) -> str:
        return click.style("✦ " + self.message, fg="red")
