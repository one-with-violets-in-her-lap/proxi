from PySide6 import QtCore, QtGui, QtWidgets

from proxi.core.models.proxy import ProxyProfile

_STATUS_CIRCLE_COLORS = {
    "active": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C3EE9D, stop:1 #86D441);",
    "disabled": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 white, stop:1 #CFCFCF);",
}


class StatusCircleWidget(QtWidgets.QFrame):
    def __init__(self, active: bool):
        super().__init__()

        self.setObjectName("statusCircle")

        self.setStyleSheet(
            "#statusCircle { border-radius: 6px;"
            + f"background-color: {_STATUS_CIRCLE_COLORS['active' if active else 'disabled']};"
            + "}"
        )

        self.setFixedSize(12, 12)
        self.resize(12, 12)


class ProxyProfileCardWidget(QtWidgets.QFrame):
    def __init__(self, proxy_profile: ProxyProfile):
        super().__init__()

        self.setObjectName("proxyProfile")

        self.setStyleSheet("""
           #proxyProfile {
               border: 1px solid rgb(219, 219, 219);
               border-radius: 10px;
               background-color: white;
               padding: 14px 20px;
               max-width: 600px;
           }
        """)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.header_layout.setSpacing(10)

        self.status_circle = StatusCircleWidget(proxy_profile.is_active)

        self.profile_title = QtWidgets.QLabel(proxy_profile.name)
        self.profile_title_font = QtGui.QFont()
        self.profile_title_font.setWeight(QtGui.QFont.Weight.Light)
        self.profile_title.setFont(self.profile_title_font)

        self.header_layout.addWidget(self.status_circle)
        self.header_layout.addWidget(self.profile_title)

        self.proxy_urls = QtWidgets.QLabel(
            self._build_proxy_urls_info_text(proxy_profile)
        )
        self.proxy_urls.setStyleSheet("""
            QLabel {
                font-weight: 300;
                color: rgb(115,115,115);
                font-size: 14px;
            }
        """)

        self.edit_button = QtWidgets.QPushButton("(*) Select")
        self.edit_button.setFixedWidth(90)
        self.edit_button.setStyleSheet("QPushButton { margin-top: 10px; }")
        self.edit_button.setVisible(not proxy_profile.is_active)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.proxy_urls)
        self.main_layout.addWidget(self.edit_button)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.main_layout)

    def _build_proxy_urls_info_text(self, proxy_profile: ProxyProfile):
        return "\n".join(
            [
                url
                for url in proxy_profile.settings.model_dump().values()
                if url is not None
            ]
        )
