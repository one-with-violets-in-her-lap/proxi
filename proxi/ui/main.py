import logging
import sys

from PySide6 import QtSvgWidgets, QtWidgets

from proxi.core.models.config import ProxiAppConfigProvider
from proxi.core.proxy_config_clients import CrossPlatformProxyConfig
from proxi.core.utils.platform import get_user_platform
from proxi.ui.widgets.drawing_decoration import DrawingDecorationWidget
from proxi.ui.widgets.proxy_profile_list import ProxyProfileListWidget
from proxi.ui.widgets.status_switch import StatusSwitch

WINDOW_WIDTH = 460
WINDOW_HEIGHT = 700


class AppWindow(QtWidgets.QMainWindow):
    def __init__(self, proxy_manager: CrossPlatformProxyConfig):
        super().__init__()

        self.setWindowTitle("Proxi")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMaximumHeight(WINDOW_HEIGHT)

        self.setObjectName("mainWindow")
        self.setStyleSheet("""
            #mainWindow {
                background-color: white;
            }
        """)

        self.drawing_image = DrawingDecorationWidget(self)

        self.logo = QtSvgWidgets.QSvgWidget("./assets/logo-light-theme.svg")
        self.logo.setFixedSize(96, 56)

        self.status_switch = StatusSwitch(proxy_manager)

        self.proxy_profile_list = ProxyProfileListWidget(proxy_manager)

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

    window = AppWindow(CrossPlatformProxyConfig(get_user_platform(), ProxiAppConfigProvider()))
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
