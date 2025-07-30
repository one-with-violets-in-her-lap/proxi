from PySide6 import QtCore, QtGui, QtWidgets


class StatusCircleWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("statusCircle")

        self.setStyleSheet("""
            #statusCircle {
                border-radius: 6px;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1, stop:0 #C3EE9D, stop:1 #86D441
                );
            }
        """)

        self.setFixedSize(12, 12)
        self.resize(12, 12)


class ProxyProfileCardWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("proxyProfile")

        self.setStyleSheet("""
           #proxyProfile {
               border: 1px solid rgb(219, 219, 219);
               border-radius: 6px;
               background-color: white;
               margin-top: 35px;
               padding: 21px;
               max-width: 600px;
           }
        """)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.header_layout.setSpacing(10)

        self.status_circle = StatusCircleWidget()

        self.profile_title = QtWidgets.QLabel("Profile 1")
        self.profile_title_font = QtGui.QFont()
        self.profile_title_font.setWeight(QtGui.QFont.Weight.Light)
        self.profile_title.setFont(self.profile_title_font)

        self.header_layout.addWidget(self.status_circle)
        self.header_layout.addWidget(self.profile_title)

        self.proxy_url = QtWidgets.QLabel("https://192.168.1.1:5603")
        self.proxy_url.setStyleSheet("""
            QLabel {
                font-weight: 300;
                color: rgb(115,115,115);
                font-size: 14px;
            }
        """)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.proxy_url)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)
