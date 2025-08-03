from PySide6 import QtWidgets

from proxi.core.models.proxy import ProxyProfile
from proxi.core.services.proxy_profiles import ProxyProfilesService
from proxi.ui.widgets.add_profile_dialog import AddProfileDialogWidget
from proxi.ui.widgets.proxy_profile import ProxyProfileCardWidget
from proxi.ui.widgets.ui_kit.button import AppButtonWidget


class ProxyProfileListWidget(QtWidgets.QWidget):
    def __init__(self, proxy_profiles_service: ProxyProfilesService):
        super().__init__()

        self.proxy_profiles_service = proxy_profiles_service

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 10, 0, 0)
        self.main_layout.setSpacing(13)

        self.add_button = AppButtonWidget("+")
        self.add_button.setFixedSize(30, 30)
        self.add_button.clicked.connect(self._create_add_profile_dialog)

        self.main_layout.addWidget(self.add_button)

        self.profile_cards: list[ProxyProfileCardWidget] = []
        self._update_card_list(self.proxy_profiles_service.get_profiles())

        self.setLayout(self.main_layout)

    def _select_profile(self, profile: ProxyProfile):
        self.proxy_profiles_service.set_profile_as_active(profile)

        self._update_card_list(self.proxy_profiles_service.get_profiles())

    def _update_card_list(self, profiles: list[ProxyProfile]):
        for card in self.profile_cards:
            self.main_layout.removeWidget(card)

        self.profile_cards = [ProxyProfileCardWidget(profile) for profile in profiles]

        for card in self.profile_cards:
            card.profile_selected.connect(self._select_profile)
            self.main_layout.addWidget(card)

        self.update()

    def _create_add_profile_dialog(self):
        dialog = AddProfileDialogWidget()

        def handle_submit(profile: ProxyProfile):
            self.proxy_profiles_service.add_profile(profile)
            self._update_card_list(self.proxy_profiles_service.get_profiles())
            dialog.accept()

        dialog.profile_added.connect(handle_submit)

        dialog.exec()
