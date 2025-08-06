import os

from proxi.core.models.proxy import SystemProxySettings
from proxi.core.proxy_config_clients._base import BaseProxyConfigClient

SHELL_SETUP_SCRIPT_PATH = os.path.expanduser("~/proxi_setup.sh")


class ShellProxyConfig(BaseProxyConfigClient):
    def get_is_proxy_active(self):
        with open(SHELL_SETUP_SCRIPT_PATH, "rt") as setup_script_read_stream:
            lines = setup_script_read_stream.read().splitlines()
            commented_lines = [line for line in lines if line.startswith("#")]

            if len(commented_lines) == len(lines):
                return False
            else:
                return True

    def set_is_proxy_active(self, is_active: bool):
        with open(SHELL_SETUP_SCRIPT_PATH, "rt") as setup_script_read_stream:
            setup_script_content = setup_script_read_stream.read()

            with open(SHELL_SETUP_SCRIPT_PATH, "wt") as setup_script_write_stream:
                print(setup_script_content)
                if is_active:
                    setup_script_write_stream.write(
                        setup_script_content.replace("# export", "export")
                    )
                else:
                    setup_script_write_stream.write(
                        setup_script_content.replace("export", "# export")
                    )

    def set_proxy_settings(self, proxy_settings):
        with open(SHELL_SETUP_SCRIPT_PATH, "wt") as setup_script_write_stream:
            http_proxy_setup_code = (
                f"export HTTP_PROXY={proxy_settings.http_proxy or ''}"
                + "\n"
                + f"export http_proxy={proxy_settings.http_proxy or ''}"
            )

            https_proxy_setup_code = (
                f"export HTTPS_PROXY={proxy_settings.https_proxy or ''}"
                + "\n"
                + f"export https_proxy={proxy_settings.https_proxy or ''}"
            )

            socks5_proxy_setup_code = (
                f"export SOCKS_PROXY={proxy_settings.socks5_proxy or ''}"
                + "\n"
                + f"export socks_proxy={proxy_settings.socks5_proxy or ''}"
            )

            setup_script_write_stream.write(
                "\n".join(
                    [
                        http_proxy_setup_code,
                        https_proxy_setup_code,
                        socks5_proxy_setup_code,
                    ]
                )
            )

    def get_proxy_settings(self):
        with open(SHELL_SETUP_SCRIPT_PATH, "rt") as setup_script_read_stream:
            lines = setup_script_read_stream.read().splitlines()

            http_proxy = None
            https_proxy = None
            socks5_proxy = None

            for line in lines:
                variable_export_start, exported_variable_value = line.split("=")

                if (
                    "HTTP_PROXY" in variable_export_start
                    and exported_variable_value != ""
                ):
                    http_proxy = exported_variable_value

                if (
                    "HTTPS_PROXY" in variable_export_start
                    and exported_variable_value != ""
                ):
                    https_proxy = exported_variable_value

                if (
                    "SOCKS_PROXY" in variable_export_start
                    and exported_variable_value != ""
                ):
                    socks5_proxy = exported_variable_value

            return SystemProxySettings.model_validate(
                {
                    "http_proxy": http_proxy,
                    "https_proxy": https_proxy,
                    "socks5_proxy": socks5_proxy,
                }
            )
