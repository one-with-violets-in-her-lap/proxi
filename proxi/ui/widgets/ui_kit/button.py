from typing import Literal

from PySide6 import QtGui, QtWidgets

AppButtonVariant = Literal["outline", "danger"]
AppButtonSize = Literal["icon", "default"]


class AppButtonWidget(QtWidgets.QPushButton):
    def __init__(
        self,
        text: str,
        variant: AppButtonVariant = "outline",
        size: AppButtonSize = "default",
    ):
        super().__init__(text)

        self.setCursor(QtGui.Qt.CursorShape.PointingHandCursor)

        self.setProperty("variant", variant)

        self.setProperty("button_size", size)
        if size == "icon":
            self.setFixedSize(30, 30)

        self.setStyleSheet("""
            QPushButton {
                font-weight: 400;
            }

            QPushButton[button_size="default"] {
                padding: 4px 15px;
            }

            QPushButton[button_size="icon"] {
                font-size: 18px;
                width: 30px;
                height: 30px;
            }

            QPushButton[variant="outline"] {
                background-color: rgb(245, 245, 245);
                border: 1px solid rgba(0, 0, 0, 0.15);
                border-radius: 6px;
            }

            QPushButton[variant="outline"]:hover {
                background-color: rgb(236, 236, 236);
            }

            QPushButton[variant="danger"] {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFE8E8, stop:1 #FFDEDE);
                color: #FF8484;
                border: 1px solid #FFA8A8;
                border-radius: 6px;
            }

            QPushButton[variant="danger"]:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFE8E8, stop:1 #FFC0C0);
            }
        """)
