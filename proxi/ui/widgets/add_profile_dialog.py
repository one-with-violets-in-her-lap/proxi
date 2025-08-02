from PySide6 import QtCore, QtWidgets

from proxi.core.models.proxy import ProxyProfile, SystemProxySettings


class AddProfileDialogWidget(QtWidgets.QDialog):
    profile_added = QtCore.Signal(ProxyProfile)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add profile")

        self.setContentsMargins(20, 20, 20, 20)
        self.resize(400, 200)

        self.action_buttons_box = QtWidgets.QDialogButtonBox()

        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setText("OK")
        self.ok_button.clicked.connect(self._handle_submit)

        self.action_buttons_box.addButton(
            "Cancel", QtWidgets.QDialogButtonBox.ButtonRole.RejectRole
        )
        self.action_buttons_box.addButton(
            self.ok_button, QtWidgets.QDialogButtonBox.ButtonRole.ActionRole
        )
        self.action_buttons_box.rejected.connect(self.reject)
        self.action_buttons_box.accepted.connect(self.accept)

        self.http_proxy_field = QtWidgets.QLineEdit(
            placeholderText="http://0.0.0.0:8000"
        )
        self.https_proxy_field = QtWidgets.QLineEdit(
            placeholderText="https://0.0.0.0:8000"
        )
        self.socks5_proxy_field = QtWidgets.QLineEdit(
            placeholderText="socks5://0.0.0.0:8000"
        )

        self.profile_name_field = QtWidgets.QLineEdit(
            placeholderText="Work",
        )

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("Name:", self.profile_name_field)
        self.form_layout.addRow("HTTP proxy:", self.http_proxy_field)
        self.form_layout.addRow("HTTPS proxy:", self.https_proxy_field)
        self.form_layout.addRow("SOCKS5 proxy:", self.socks5_proxy_field)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.action_buttons_box)

        self.setLayout(self.main_layout)

    def _handle_submit(self):
        self.profile_added.emit(
            ProxyProfile(
                name=self.profile_name_field.text(),
                is_active=False,
                settings=SystemProxySettings(
                    http_proxy=self.http_proxy_field.text() or None,
                    https_proxy=self.https_proxy_field.text() or None,
                    socks5_proxy=self.socks5_proxy_field.text() or None,
                ),
            )
        )
