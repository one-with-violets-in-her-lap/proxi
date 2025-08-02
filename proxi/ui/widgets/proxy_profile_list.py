from PySide6 import QtWidgets

from proxi.core.models.proxy import ProxyProfile
from proxi.core.proxy_managers import ProxyManager
from proxi.ui.widgets.proxy_profile import ProxyProfileCardWidget
from proxi.ui.widgets.ui_kit.button import AppButtonWidget


class ProxyProfileListWidget(QtWidgets.QWidget):
    def __init__(self, proxy_manager: ProxyManager):
        super().__init__()

        self.proxy_manager = proxy_manager

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 34, 0, 0)
        self.main_layout.setSpacing(13)

        self.add_button = AppButtonWidget("+")
        self.add_button.setFixedSize(30, 30)

        self.main_layout.addWidget(self.add_button)

        self.profile_cards: list[ProxyProfileCardWidget] = []
        self._update_card_list(proxy_manager.get_profiles())

        self.setLayout(self.main_layout)

    def _select_profile(self, profile: ProxyProfile):
        self.proxy_manager.set_active_profile(
            profile, do_before_settings_save=self._update_card_list
        )

    def _update_card_list(self, profiles: list[ProxyProfile]):
        for card in self.profile_cards:
            self.main_layout.removeWidget(card)

        self.profile_cards = [ProxyProfileCardWidget(profile) for profile in profiles]

        for card in self.profile_cards:
            card.profile_selected.connect(self._select_profile)
            self.main_layout.addWidget(card)
