import bank_admins
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from errors import *

Application = QApplication(sys.argv)

class Login(QWidget):
    def __init__(self, login_function):
        self.login_function = login_function

        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: #333333;
            }
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border-radius: 5px;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0061A7;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        email_layout = QVBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        password_layout = QVBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        layout.addLayout(email_layout)
        layout.addLayout(password_layout)

        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        account_number, success = self.login_function(f"'{email}'", f"'{password}'")

        if success and account_number != bank_admins.BANK_ADMIN:
            print("Logged In! \n", "Account: ", account_number)
        else:
            print(account_number, "\n", success)
        
        self.email_input.clear()
        self.password_input.clear()
