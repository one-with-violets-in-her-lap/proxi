from PySide6 import QtWidgets

from proxi.core.proxy_managers import ProxyManager
from proxi.ui.widgets.proxy_profile import ProxyProfileCardWidget


class ProxyProfileListWidget(QtWidgets.QWidget):
    def __init__(self, proxy_manager: ProxyManager):
        super().__init__()

        self.profile_manager = proxy_manager

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 34, 0, 0)
        self.main_layout.setSpacing(13)

        self.profiles = proxy_manager.get_profiles()
        self.profile_cards = [
            ProxyProfileCardWidget(profile) for profile in self.profiles
        ]

        for card in self.profile_cards:
            self.main_layout.addWidget(card)

        self.setLayout(self.main_layout)
