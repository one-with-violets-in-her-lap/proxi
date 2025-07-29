from PySide6 import QtGui, QtWidgets


class DrawingDecorationWidget(QtWidgets.QLabel):
    def __init__(self, parent_widget: QtWidgets.QWidget):
        super().__init__(parent_widget)

        self.parent_widget = parent_widget

        self.setFixedSize(147, 232)
        self.setPixmap(QtGui.QPixmap("./assets/drawing.jpg"))
        self.move(parent_widget.width() - self.width() - 20, 20)

    def update_position_on_parent_resize(self):
        self.move(self.parent_widget.width() - self.width() - 20, 20)
