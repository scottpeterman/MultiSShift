from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QFileDialog)

class AdhocConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ad-hoc SSH Connection")
        self.parent = parent
        layout = QVBoxLayout(self)

        # Authentication Type Radio Buttons
        self.auth_type_group = QButtonGroup(self)
        password_button = QRadioButton("Password")
        key_button = QRadioButton("SSH Key")
        self.auth_type_group.addButton(password_button, 1)
        self.auth_type_group.addButton(key_button, 2)
        layout.addWidget(password_button)
        layout.addWidget(key_button)
        password_button.setChecked(True)  # Set default to password authentication
        if parent.settings is not None and isinstance(parent.settings, dict):
            settings = parent.settings['defaults']
            host = settings.get("host","")
            port = settings.get("port","22")
            username = settings.get("username", "")
            key_path = settings.get("key_path", "")
        else:
            host = ""
            port = "22"
            username = ""
            key_path = ""
        # Host Field
        self.host_edit = QLineEdit(self)
        self.host_edit.setText(host)
        layout.addWidget(QLabel("Host:"))
        layout.addWidget(self.host_edit)

        # Port Field
        self.port_edit = QLineEdit(self)
        self.port_edit.setText(str(port))
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_edit)

        # Username Field
        self.username_edit = QLineEdit(self)
        self.username_edit.setText(username)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)

        # Password Field
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)

        # SSH Key File Path Field
        self.key_edit = QLineEdit(self)
        self.key_edit.setText(key_path)
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_key_file)
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("SSH Key File:"))
        key_layout.addWidget(self.key_edit)
        key_layout.addWidget(self.browse_button)
        layout.addLayout(key_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        connect_button = QPushButton("Connect", self)
        connect_button.clicked.connect(self.accept)
        connect_button.setDefault(True)
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(connect_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def browse_key_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select SSH Key File")
        if file_name:
            self.key_edit.setText(file_name)

    def get_connection_details(self):
        auth_type = 'password' if self.auth_type_group.checkedId() == 1 else 'key'
        return {
            "host": self.host_edit.text(),
            "port": self.port_edit.text(),
            "username": self.username_edit.text(),
            "auth_type": auth_type,
            "auth": self.password_edit.text() if auth_type == 'password' else self.key_edit.text()
        }
