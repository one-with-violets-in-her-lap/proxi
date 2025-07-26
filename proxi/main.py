import sys

from PySide6 import QtWidgets


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Set proxy")

        self.box_layout = QtWidgets.QVBoxLayout(self)
        self.box_layout.addWidget(self.button)
        self.setLayout(self.box_layout)


def main():
    app = QtWidgets.QApplication([])

    main_widget = MainWidget()
    main_widget.resize(800, 600)
    main_widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
