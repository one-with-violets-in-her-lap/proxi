from PySide6 import QtGui, QtWidgets


class AppButtonWidget(QtWidgets.QPushButton):
    def __init__(self, text: str):
        super().__init__(text)

        self.setCursor(QtGui.Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet("""
            QPushButton {
                background-color: rgb(245, 245, 245);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: rgb(233, 233, 233);
            }
        """)
