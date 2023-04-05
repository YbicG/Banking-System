import bank_admins
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from errors import *

Application = QApplication(sys.argv)

ACCOUNT_NUMBER = None

def display_error(error_type: CustomError):
    message_box = QMessageBox()

    message_box.setWindowTitle(error_type)
    message_box.setMinimumSize(200, 200)
    if error_type == NOT_FOUND:
        message_box.setText("Account not found!")
    elif error_type == ALREADY_EXISTS:
        message_box.setText("Account already exists!")
    elif error_type == INVALID_PROTOCOL:
        message_box.setText("Incorrect information given!")
    elif error_type == CLIENT_DENIED:
        message_box.setText("Unable to connect to database!")
    elif error_type == NOT_ENOUGH_FUNDS:
        message_box.setText("Not enough money in balance!")
    else:
        message_box.setText(error_type)

    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

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
            ACCOUNT_NUMBER = account_number
            print("Logged In! \n", "Account: ", account_number)
        else:
            display_error(account_number)
            print(account_number, "\n", success)
        
        self.email_input.clear()
        self.password_input.clear()
