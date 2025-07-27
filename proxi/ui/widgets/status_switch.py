from PySide6 import QtGui, QtWidgets

from proxi.ui.widgets.switch import SwitchButton


class StatusSwitch(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label_font = QtGui.QFont()
        self.label_font.setWeight(QtGui.QFont.Weight.Light)
        self.label_font.setPixelSize(14)

        self.status_switch_widget_layout = QtWidgets.QVBoxLayout()
        self.status_switch_widget_layout.setSpacing(4)
        self.status_switch_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.switch = SwitchButton()
        self.label = QtWidgets.QLabel()
        self.label.setText("Proxy preferences enabled")
        self.label.setFont(self.label_font)

        self.status_switch_widget_layout.addWidget(self.label)
        self.status_switch_widget_layout.addWidget(self.switch)

        self.setLayout(self.status_switch_widget_layout)
