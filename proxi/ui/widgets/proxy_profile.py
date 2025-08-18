from PySide6 import QtCore, QtGui, QtSvgWidgets, QtWidgets

from proxi.core.models.proxy import ProxyProfile
from proxi.ui.executable_path import build_path_from_executable
from proxi.ui.widgets.ui_kit.button import AppButtonWidget

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
    profile_selected = QtCore.Signal(ProxyProfile)
    profile_deleted = QtCore.Signal(ProxyProfile)
    profile_edit_requested = QtCore.Signal(ProxyProfile)

    def __init__(self, proxy_profile: ProxyProfile):
        super().__init__()

        self.setObjectName("proxyProfile")

        self.setStyleSheet("""
           #proxyProfile {
               border: 1px solid rgb(219, 219, 219);
               border-radius: 10px;
               background-color: white;
               padding: 12px 20px;
               max-width: 400px;
           }
        """)

        self.globe_decoration = QtSvgWidgets.QSvgWidget(
            build_path_from_executable("assets/web-globe.svg")
        )
        self.globe_decoration.setFixedSize(156, 156)
        self.globe_decoration.setParent(self)

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
        self.proxy_urls.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.select_button = AppButtonWidget("Select")
        self.select_button.setVisible(not proxy_profile.is_active)
        self.select_button.clicked.connect(
            lambda: self.profile_selected.emit(proxy_profile)
        )
        self.select_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.edit_icon = QtGui.QIcon(build_path_from_executable("assets/settings.svg"))

        self.edit_button = AppButtonWidget("", size="icon")
        self.edit_button.setToolTip("Edit")
        self.edit_button.setIcon(self.edit_icon)
        self.edit_button.clicked.connect(
            lambda: self.profile_edit_requested.emit(proxy_profile)
        )

        self.trash_can_icon = QtGui.QIcon(
            build_path_from_executable("assets/trash.svg")
        )

        self.delete_button = AppButtonWidget("", variant="danger", size="icon")
        self.delete_button.setIcon(self.trash_can_icon)
        self.delete_button.setToolTip("Delete")
        self.delete_button.setVisible(not proxy_profile.is_active)
        self.delete_button.clicked.connect(
            lambda: self.profile_deleted.emit(proxy_profile)
        )

        self.action_buttons_layout = QtWidgets.QHBoxLayout()
        self.action_buttons_layout.addWidget(self.select_button)
        self.action_buttons_layout.addWidget(self.edit_button)
        self.action_buttons_layout.addWidget(self.delete_button)
        self.action_buttons_layout.setAlignment(QtGui.Qt.AlignmentFlag.AlignLeft)

        if not proxy_profile.is_active:
            self.globe_decoration.setGraphicsEffect(
                QtWidgets.QGraphicsOpacityEffect(self, opacity=0.5)
            )
            self.profile_title.setGraphicsEffect(
                QtWidgets.QGraphicsOpacityEffect(self, opacity=0.7)
            )

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.proxy_urls)
        self.main_layout.addLayout(self.action_buttons_layout)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.setLayout(self.main_layout)

        self.globe_decoration.move(
            230, self.sizeHint().height() - self.globe_decoration.height() // 2
        )

    def _build_proxy_urls_info_text(self, proxy_profile: ProxyProfile):
        return "\n".join(
            [
                str(url)
                for url in proxy_profile.settings.model_dump().values()
                if url is not None
            ]
        )
