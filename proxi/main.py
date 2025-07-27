import sys

from PySide6 import QtSvgWidgets, QtWidgets

WINDOW_WIDTH = 460
WINDOW_HEIGHT = 700


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Set proxy")

        self.logo = QtSvgWidgets.QSvgWidget("./assets/logo-light-theme.svg")
        self.logo.setFixedSize(96, 56)

        self.box_layout = QtWidgets.QVBoxLayout(self)
        self.box_layout.addWidget(self.logo)
        self.box_layout.addWidget(self.button)
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
