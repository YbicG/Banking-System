import bank_admins
import database as db
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from errors import *

Application = QApplication(sys.argv)

# GLOBAL VARIABLES
ACCOUNT_NUMBER = None
BALANCE = None
HOME_PAGE = None
WITHDRAW_PAGE = None
DEPOSIT_PAGE = None
SETTINGS_PAGE = None
#
 
def display_error(error_type: CustomError):
    message_box = QMessageBox()

    message_box.setWindowTitle(error_type)
    message_box.setMinimumSize(200, 200)
    if error_type == NOT_FOUND:
        message_box.setText("Account not found!")
    elif error_type == ALREADY_EXISTS:
        message_box.setText("Account already exists!")
    elif error_type == INVALID_PROTOCOL:
        message_box.setText("Incorrect password given!")
    elif error_type == CLIENT_DENIED:
        message_box.setText("Unable to connect to database!")
    elif error_type == NOT_ENOUGH_FUNDS:
        message_box.setText("Not enough money in balance!")
    elif error_type == WRONG_DATA_TYPE:
        message_box.setText("Wrong data type submited! Try using an integer or number above 0!")
    else:
        message_box.setText(error_type)

    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

def display_success(message):
    message_box = QMessageBox()
    message_box.setWindowTitle("Sucess!")
    message_box.setMinimumSize(200, 200)
    
    message_box.setText(message)
    
    message_box.setIcon(QMessageBox.Icon.Information)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

class Login(QWidget):
    def __init__(self, login_function):
        self.login_function = login_function

        super().__init__()
        self.setWindowTitle("CL Banking - Login")
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
        self.email_input.setPlaceholderText("example@domain.com")
        

        password_layout = QVBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
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
            global ACCOUNT_NUMBER
            global HOME_PAGE
            ACCOUNT_NUMBER = account_number

            self.email_input.clear()
            self.password_input.clear()
            print("Logged In! \n", "Account: ", account_number)

            HOME_PAGE = Homepage()
            HOME_PAGE.show()

            self.hide()
        else:
            display_error(account_number)
            self.email_input.clear()
            self.password_input.clear()

class Homepage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CL Banking - Home Page")
        self.setMinimumSize(960, 540)
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
            }
            QLabel {
                font-size: 50px;
                color: #333333;
                font-weight: bold;
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
        self.setLayout(layout)

        ## GETTING THE BALANCE
        print(ACCOUNT_NUMBER)
        balance, success = db.get_from_user(ACCOUNT_NUMBER, "balance")

        if success:

            global BALANCE
            BALANCE = balance[0]
            print(balance)
            balance = "Balance: $"+str(balance[0])

        else:
            balance = CLIENT_DENIED
        ##

        balance_label = QLabel(balance)
        balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        withdraw_button = QPushButton("Withdraw")
        withdraw_button.clicked.connect(self.withdraw)

        deposit_button = QPushButton("Deposit")
        deposit_button.clicked.connect(self.deposit)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.settings)

        layout.addWidget(balance_label)
        layout.addWidget(withdraw_button)
        layout.addWidget(deposit_button)
        layout.addWidget(settings_button)

    def withdraw(self):
        global WITHDRAW_PAGE

        WITHDRAW_PAGE = Withdraw()
        WITHDRAW_PAGE.show()
        self.hide()


    def deposit(self):
        global DEPOSIT_PAGE

        DEPOSIT_PAGE = Deposit()
        DEPOSIT_PAGE.show()
        self.hide()

    def settings(self):
        print("Settings button clicked")

class Withdraw(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CL Banking - Withdraw")
        self.setMinimumSize(400, 200)
        self.setStyleSheet('''
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
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background-color: #CCCCCC;
            }
        ''')

        layout = QVBoxLayout()
        self.setLayout(layout)

        balance_layout = QHBoxLayout()

        back_button = QToolButton()
        back_button.setIcon(QIcon("C:\\Users\\CJ Lester\\Downloads\\Code Workspace\\Python\\BankingSystem\\Library\\back_arrow.png"))
        back_button.clicked.connect(self.back)

        self.balance_label = QLabel("Balance: $"+str(BALANCE))
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balance_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.withdraw_input = QLineEdit()
        self.withdraw_input.setPlaceholderText("Enter amount to withdraw")

        withdraw_button = QPushButton("Withdraw")
        withdraw_button.clicked.connect(self.withdraw)

        balance_layout.addWidget(back_button)
        balance_layout.addStretch()
        balance_layout.addWidget(self.balance_label)
        balance_layout.addStretch()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.withdraw_input)
        input_layout.addWidget(withdraw_button)

        layout.addLayout(balance_layout)
        layout.addStretch()
        layout.addLayout(input_layout)

    def back(self):
        global HOME_PAGE

        HOME_PAGE = Homepage()
        HOME_PAGE.show()
        self.hide()

    def withdraw(self):
        global BALANCE

        withdraw_amount = self.withdraw_input.text()

        try:
            withdraw_amount = float(withdraw_amount)
        except:
            display_error(WRONG_DATA_TYPE)
            return
        
        if withdraw_amount <= 0:
            display_error(WRONG_DATA_TYPE)
            return

        result, success = db.withdraw(ACCOUNT_NUMBER, withdraw_amount)

        if success:
            self.balance_label.setText("Balance: $"+str(BALANCE-withdraw_amount))
            BALANCE -= withdraw_amount
            display_success("Successfuly withdrew $"+str(withdraw_amount)+" from your account!")

        else:
            display_error(result)
        
        self.withdraw_input.clear()

class Deposit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CL Banking - Deposit")
        self.setMinimumSize(400, 200)
        self.setStyleSheet('''
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
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background-color: #CCCCCC;
            }
        ''')

        layout = QVBoxLayout()
        self.setLayout(layout)

        balance_layout = QHBoxLayout()

        back_button = QToolButton()
        back_button.setIcon(QIcon("C:\\Users\\CJ Lester\\Downloads\\Code Workspace\\Python\\BankingSystem\\Library\\back_arrow.png"))
        back_button.clicked.connect(self.back)

        self.balance_label = QLabel("Balance: $"+str(BALANCE))
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balance_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.deposit_input = QLineEdit()
        self.deposit_input.setPlaceholderText("Enter amount to deposit")

        deposit_button = QPushButton("Deposit")
        deposit_button.clicked.connect(self.deposit)

        balance_layout.addWidget(back_button)
        balance_layout.addStretch()
        balance_layout.addWidget(self.balance_label)
        balance_layout.addStretch()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.deposit_input)
        input_layout.addWidget(deposit_button)

        layout.addLayout(balance_layout)
        layout.addStretch()
        layout.addLayout(input_layout)

    def back(self):
        global HOME_PAGE

        HOME_PAGE = Homepage()
        HOME_PAGE.show()
        self.hide()

    def deposit(self):
        global BALANCE

        deposit_amount = self.deposit_input.text()

        try:
            deposit_amount = float(deposit_amount)
        except:
            display_error(WRONG_DATA_TYPE)
            return
        
        if deposit_amount <= 0:
            display_error(WRONG_DATA_TYPE)
            return
        
        result, success = db.deposit(ACCOUNT_NUMBER, deposit_amount)
        if success:
            self.balance_label.setText("Balance: $"+str(BALANCE+deposit_amount))
            BALANCE += deposit_amount
            display_success("Successfuly deposited $"+str(deposit_amount)+" into your account!")
        else:
            display_error(result)
        
        self.deposit_input.clear()