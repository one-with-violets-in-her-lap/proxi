from PySide6 import QtGui, QtWidgets

from proxi.core.proxy_config_clients import CrossPlatformProxyConfig
from proxi.ui.widgets.ui_kit.switch import AppSwitchButton


class StatusSwitch(QtWidgets.QWidget):
    def __init__(self, proxy_manager: CrossPlatformProxyConfig):
        super().__init__()

        self.proxy_manager = proxy_manager

        self.label_font = QtGui.QFont()
        self.label_font.setWeight(QtGui.QFont.Weight.Light)
        self.label_font.setPixelSize(14)

        self.status_switch_widget_layout = QtWidgets.QVBoxLayout()
        self.status_switch_widget_layout.setSpacing(4)
        self.status_switch_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.switch = AppSwitchButton()
        self.switch.setChecked(self.proxy_manager.get_is_proxy_active())
        self.switch.toggled.connect(
            lambda is_toggled: self.proxy_manager.set_is_proxy_active(is_toggled)
        )

        self.label = QtWidgets.QLabel()
        self.label.setText("Proxy preferences enabled")
        self.label.setFont(self.label_font)

        self.status_switch_widget_layout.addWidget(self.label)
        self.status_switch_widget_layout.addWidget(self.switch)

        self.setLayout(self.status_switch_widget_layout)
