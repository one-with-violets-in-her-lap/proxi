from pydantic import ValidationError
from PySide6 import QtCore, QtWidgets

from proxi.core.models.proxy import ProxyProfile

_ERROR_MESSAGES_BY_FIELD_LOC = {
    ("name",): "Profile name is invalid",
    ("settings", "http_proxy"): "HTTP proxy URL is invalid",
    ("settings", "https_proxy"): "HTTPS proxy URL is invalid",
    ("settings", "socks5_proxy"): "SOCKS5 proxy URL is invalid",
    ("settings",): "At least one proxy must be specified",
}


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

        self.error_label = QtWidgets.QLabel()
        self.error_label.setStyleSheet("""
            QLabel {
                color: #ed5e5e;
                font-size: 14px;
                font-weight: 400;
                margin-top: 10px;
            }
        """)
        self.error_label.setVisible(False)
        self.error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.action_buttons_box)
        self.main_layout.addWidget(self.error_label)

        self.setLayout(self.main_layout)

    def show_error(self, text: str):
        self.error_label.setText(text)
        self.error_label.setVisible(True)

    def _handle_submit(self):
        try:
            self.profile_added.emit(
                ProxyProfile.model_validate(
                    dict(
                        name=self.profile_name_field.text() or None,
                        is_active=False,
                        settings=dict(
                            http_proxy=self.http_proxy_field.text() or None,
                            https_proxy=self.https_proxy_field.text() or None,
                            socks5_proxy=self.socks5_proxy_field.text() or None,
                        ),
                    )
                )
            )
        except ValidationError as validation_error:
            first_error = validation_error.errors()[0]

            self.show_error(
                _ERROR_MESSAGES_BY_FIELD_LOC.get(first_error["loc"])
                or first_error["msg"]
            )
        except Exception as error:
            self.show_error("An unknown error occurred")
            raise error
