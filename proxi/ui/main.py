import logging
import sys

from PySide6 import QtSvgWidgets, QtWidgets

from proxi.core.models.config import ProxiAppConfigProvider
from proxi.core.proxy_config_clients import CrossPlatformProxyConfig
from proxi.core.services.proxy_profiles import ProxyProfilesService
from proxi.core.utils.platform import get_user_settings_platform
from proxi.ui.executable_path import build_path_from_executable
from proxi.ui.widgets.drawing_decoration import DrawingDecorationWidget
from proxi.ui.widgets.proxy_profile_list import ProxyProfileListWidget
from proxi.ui.widgets.status_switch import StatusSwitch

WINDOW_MIN_WIDTH = 460
WINDOW_HEIGHT = 700


class AppWindow(QtWidgets.QMainWindow):
    def __init__(
        self,
        proxy_config: CrossPlatformProxyConfig,
        proxy_profiles_service: ProxyProfilesService,
    ):
        super().__init__()

        self.setWindowTitle("Proxí")

        self.resize(WINDOW_MIN_WIDTH, WINDOW_HEIGHT)
        self.setMaximumHeight(WINDOW_HEIGHT)
        self.setMinimumWidth(460)

        self.setObjectName("mainWindow")
        self.setStyleSheet("""
            #mainWindow {
                background-color: white;
            }
        """)

        self.drawing_image = DrawingDecorationWidget(self)

        self.logo = QtSvgWidgets.QSvgWidget(
            build_path_from_executable("assets/logo-light-theme.svg")
        )
        self.logo.setFixedSize(96, 56)

        self.status_switch = StatusSwitch(proxy_config)

        self.proxy_profile_list = ProxyProfileListWidget(proxy_profiles_service)

        self.main_content_layout = QtWidgets.QVBoxLayout()
        self.main_content_layout.addWidget(self.logo)
        self.main_content_layout.addWidget(self.status_switch)
        self.main_content_layout.addWidget(self.proxy_profile_list)

        self.main_content_layout.addStretch(0)
        self.main_content_layout.setContentsMargins(25, 25, 25, 25)
        self.main_content_layout.setSpacing(20)

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.main_content_layout)
        self.setCentralWidget(self.main_widget)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.drawing_image.update_position_on_parent_resize()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: [%(levelname)s] %(name)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        force=True,
    )

    app = QtWidgets.QApplication([])

    app_config_provider = ProxiAppConfigProvider()
    proxy_config = CrossPlatformProxyConfig(get_user_settings_platform())
    proxy_profiles_service = ProxyProfilesService(app_config_provider, proxy_config)

    window = AppWindow(proxy_config, proxy_profiles_service)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
