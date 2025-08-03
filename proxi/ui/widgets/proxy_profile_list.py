from PySide6 import QtGui, QtWidgets

from proxi.core.models.proxy import ProxyProfile
from proxi.core.services.proxy_profiles import ProxyProfilesService
from proxi.ui.widgets.add_profile_dialog import AddProfileDialogWidget
from proxi.ui.widgets.proxy_profile import ProxyProfileCardWidget
from proxi.ui.widgets.ui_kit.button import AppButtonWidget
from proxi.ui.widgets.ui_kit.scroll_area import AppScrollArea


class ProxyProfileListWidget(QtWidgets.QWidget):
    def __init__(self, proxy_profiles_service: ProxyProfilesService):
        super().__init__()

        self.proxy_profiles_service = proxy_profiles_service

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 10, 0, 0)
        self.main_layout.setSpacing(12)

        self.add_button = AppButtonWidget("+", size="icon")
        self.add_button.clicked.connect(self._create_add_profile_dialog)

        self.profile_list_layout = QtWidgets.QVBoxLayout()
        self.profile_list_layout.setAlignment(QtGui.Qt.AlignmentFlag.AlignTop)

        self.profile_list = QtWidgets.QWidget()
        self.profile_list.setLayout(self.profile_list_layout)

        self.profile_list_scroll_area = AppScrollArea(self.profile_list)
        self.profile_list_scroll_area.setMinimumHeight(self.window().height())

        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.profile_list_scroll_area)

        self.profile_cards: list[ProxyProfileCardWidget] = []
        self._update_card_list(self.proxy_profiles_service.get_profiles())

        self.setLayout(self.main_layout)

    def _update_card_list(self, profiles: list[ProxyProfile]):
        for card in self.profile_cards:
            card.deleteLater()

        self.profile_cards = [ProxyProfileCardWidget(profile) for profile in profiles]

        for card in self.profile_cards:
            card.profile_selected.connect(self._handle_profile_select)
            card.profile_deleted.connect(self._handle_profile_delete)
            self.profile_list_layout.addWidget(card)

        self.profile_list_scroll_area.update()

    def _create_add_profile_dialog(self):
        dialog = AddProfileDialogWidget()

        def handle_submit(profile: ProxyProfile):
            self.proxy_profiles_service.add_profile(profile)
            self._update_card_list(self.proxy_profiles_service.get_profiles())
            dialog.accept()

        dialog.profile_added.connect(handle_submit)

        dialog.exec()

    def _handle_profile_select(self, profile: ProxyProfile):
        self.proxy_profiles_service.set_profile_as_active(profile)

        self._update_card_list(self.proxy_profiles_service.get_profiles())

    def _handle_profile_delete(self, profile: ProxyProfile):
        self.proxy_profiles_service.delete_profile(profile)

        self._update_card_list(self.proxy_profiles_service.get_profiles())
