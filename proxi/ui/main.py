import logging
import sys

from PySide6 import QtSvgWidgets, QtWidgets

from proxi.core.proxy_managers import ProxyManager
from proxi.core.utils.platform import get_user_platform
from proxi.ui.widgets.status_switch import StatusSwitch

WINDOW_WIDTH = 460
WINDOW_HEIGHT = 700


class MainWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainWidget")

        # TODO: come up with a better way to apply css
        self.setStyleSheet("#mainWidget {background-color:white;}")

        self.logo = QtSvgWidgets.QSvgWidget("./assets/logo-light-theme.svg")
        self.logo.setFixedSize(96, 56)

        self.status_switch = StatusSwitch(ProxyManager(get_user_platform()))

        self.box_layout = QtWidgets.QVBoxLayout(self)
        self.box_layout.addWidget(self.logo)
        self.box_layout.addWidget(self.status_switch)
        self.box_layout.addStretch(0)
        self.box_layout.setSpacing(20)

        self.setLayout(self.box_layout)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: [%(levelname)s] %(name)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        force=True,
    )

    app = QtWidgets.QApplication([])

    main_widget = MainWidget()
    main_widget.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    main_widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
