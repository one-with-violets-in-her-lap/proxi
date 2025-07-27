import sys

from PySide6 import QtSvgWidgets, QtWidgets

from proxi.ui.switch_widget import ToggleSwitchButton

WINDOW_WIDTH = 460
WINDOW_HEIGHT = 700


class MainWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainWidget")

        # TODO: come up with a better way to apply css
        self.setStyleSheet("#mainWidget {background-color:white;}")

        # TODO: move to a separate module
        self.active_switch_container = QtWidgets.QWidget()
        self.active_switch_layout = QtWidgets.QHBoxLayout()
        self.active_switch_layout.setSpacing(12)
        self.active_switch_layout.setContentsMargins(0, 0, 0, 0)

        self.active_switch = ToggleSwitchButton()
        self.active_switch_label = QtWidgets.QLabel()
        self.active_switch_label.setText("Proxy preferences enabled")

        self.active_switch_layout.addWidget(self.active_switch)
        self.active_switch_layout.addWidget(self.active_switch_label)

        self.active_switch_container.setLayout(self.active_switch_layout)

        self.logo = QtSvgWidgets.QSvgWidget("./assets/logo-light-theme.svg")
        self.logo.setFixedSize(96, 56)

        self.box_layout = QtWidgets.QVBoxLayout(self)
        self.box_layout.addWidget(self.logo)
        self.box_layout.addWidget(self.active_switch_container)
        self.box_layout.addStretch(0)
        self.box_layout.setSpacing(20)

        self.setLayout(self.box_layout)


def main():
    app = QtWidgets.QApplication([])

    main_widget = MainWidget()
    main_widget.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    main_widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
