import bank_admins
import database as db
import sys
import datetime
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from errors import *

Application = QApplication(sys.argv)

# GLOBAL VARIABLES
LOGIN = None
ACCOUNT_NUMBER = None
BALANCE = None
HOME_PAGE = None
WITHDRAW_PAGE = None
DEPOSIT_PAGE = None
SETTINGS_PAGE = None

### ADMIN

ADMIN_PAGE = None
CREATE_PAGE = None
MODIFY_PAGE = None
DELETE_PAGE = None
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

def display_message(title, message):
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setIcon(QMessageBox.Icon.Information)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()
    
def display_custom_error(title, message):
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setIcon(QMessageBox.Icon.Critical)
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

            HOME_PAGE = Homepage()
            HOME_PAGE.show()

            self.hide()
        elif success and account_number == bank_admins.BANK_ADMIN:
            global ADMIN_PAGE

            self.email_input.clear()
            self.password_input.clear()

            ADMIN_PAGE = AdminGUI()
            ADMIN_PAGE.show()

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
        balance, success = db.get_from_user(ACCOUNT_NUMBER, "balance")

        if success:

            global BALANCE
            BALANCE = balance[0]
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
        global SETTINGS_PAGE

        SETTINGS_PAGE = Settings()
        SETTINGS_PAGE.show()
        self.hide()

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

class Settings(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setFixedSize(400, 450)
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

            QToolButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background-color: #CCCCCC;
            }

            QPushButton:hover {
                background-color: #0061A7;
            }
        ''')

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        

        header = QHBoxLayout()

        title_label = QLabel("Change Settings")
        title_label.setFont(QFont("Arial"))
        title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setMargin(50)

        back_button = QToolButton()
        back_button.setIcon(QIcon("C:\\Users\\CJ Lester\\Downloads\\Code Workspace\\Python\\BankingSystem\\Library\\back_arrow.png"))
        back_button.clicked.connect(self.back)
        header.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        form_layout = QFormLayout()
        form_layout.addWidget(title_label)
        form_layout.setHorizontalSpacing(3)

        fname, success = db.get_from_user(ACCOUNT_NUMBER, "first_name")
        lname, success = db.get_from_user(ACCOUNT_NUMBER, "last_name")
        em, success = db.get_from_user(ACCOUNT_NUMBER, "email")
        dob, success = db.get_from_user(ACCOUNT_NUMBER, "date_of_birth")

        if success:
            name = QLabel("Name: "+fname[0]+" "+lname[0])
            name.setAlignment(Qt.AlignmentFlag.AlignLeft)
            main_layout.addWidget(name)

            email = QLabel("Email: "+em[0])
            email.setAlignment(Qt.AlignmentFlag.AlignLeft)
            main_layout.addWidget(email)

            dob = QLabel("Birthday: "+str(dob[0].year)+"-"+str(dob[0].month)+"-"+str(dob[0].day))
            dob.setAlignment(Qt.AlignmentFlag.AlignLeft)
            main_layout.addWidget(dob)

        account_number = QLabel("Account Number: "+str(ACCOUNT_NUMBER))
        account_number.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(account_number)

        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("John Doe")

        form_layout.addRow(name_label, self.name_input)


        birthday_label = QLabel("DOB:")
        self.birthday_input = QLineEdit()
        self.birthday_input.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow(birthday_label, self.birthday_input)

        pin_label = QLabel("PIN:")
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("XXXX")
        form_layout.addRow(pin_label, self.pin_input)

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@domain.com")
        form_layout.addRow(email_label, self.email_input)

        close_account_label = QLabel("")
        self.close_account_button = QPushButton("Close Account")
        self.close_account_button.setStyleSheet("QPushButton { background-color: #E34234; color: #FFFFFF; border-radius: 5px; font-size: 14px; padding: 8px; } QPushButton:hover { background-color: #b82619; }")
        form_layout.addRow(close_account_label, self.close_account_button)
        self.close_account_button.clicked.connect(self.close_account)
        
        button_layout = QHBoxLayout()
    
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        signout_button = QPushButton("Signout")
        signout_button.clicked.connect(self.signout)
        signout_button.setMinimumWidth(285)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_changes)

        button_layout.addWidget(signout_button)
        button_layout.addWidget(save_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def back(self):
        global HOME_PAGE

        HOME_PAGE = Homepage()
        HOME_PAGE.show()
        self.hide()

    def signout(self):
        global LOGIN

        LOGIN = Login(db.login)
        LOGIN.show()
        self.hide()

    def save_changes(self):

        name = self.name_input.text()
        birthday = self.birthday_input.text()
        pin = self.pin_input.text()
        email = self.email_input.text()

        valid = check_information(name, birthday, pin, email)

        if valid:
            global HOME_PAGE

            success = False
            result = "NO CHANGES MADE"

            text, boolean = QInputDialog.getText(None, "Pin", "Enter your pin:", echo=QLineEdit.EchoMode.Password)

            if boolean:

                try:
                    int(text)
                except:
                    display_error(WRONG_DATA_TYPE)
                    return
                
                p, s = db.get_from_user(ACCOUNT_NUMBER, "pin")

                if s:

                    if int(p[0]) == int(text):
                        pass
                    else:
                        display_custom_error("UNAUTHORIZED", "Incorrect pin number!")
                        return
                else:
                    display_error(p)
                    return 

            if len(name) != 0:

                fname = name.split(" ")[0]
                lname = name.split(" ")[1]

                result, success = db.save_to_user(ACCOUNT_NUMBER, "first_name", f"'{fname}'")
                result, success = db.save_to_user(ACCOUNT_NUMBER, "last_name", f"'{lname}'")

            if len(birthday) != 0:
                result, success = db.save_to_user(ACCOUNT_NUMBER, "date_of_birth", f"'{birthday}'")
            if len(str(pin)) != 0:
                result, success = db.save_to_user(ACCOUNT_NUMBER, "pin", pin)
            if len(email) != 0:
                result, success = db.save_to_user(ACCOUNT_NUMBER, "email", f"'{email}'")

            
            if success:   
                display_message("Changes Saved", "Your changes have been saved")
            else:
                display_error(result)

            HOME_PAGE = Homepage()
            HOME_PAGE.show()
            self.hide()


    def close_account(self):

        text, boolean = QInputDialog.getText(None, "Pin", "Enter your pin:", echo=QLineEdit.EchoMode.Password)

        if boolean:

            try:
                int(text)
            except:
                display_error(WRONG_DATA_TYPE)
                return
                
            p, s = db.get_from_user(ACCOUNT_NUMBER, "pin")

            if s:

                if int(p[0]) == int(text):
                    pass
                else:
                    display_custom_error("UNAUTHORIZED", "Incorrect pin number!")
                    return
            else:
                display_error(p)
                return 
                
        result, success = db.delete_user(ACCOUNT_NUMBER, int(text))

        if success:
            display_success("Account Deleted!")
            global LOGIN
            
            LOGIN = Login(db.login)
            LOGIN.show()
            self.hide()

def check_information(name, birthday, pin, email):
    if len(name) != 0:
            try:
                split = name.split(" ")
                fname = split[0]
                lname = split[1]
            except:
                display_message("INVALID NAME", "Invalid name! Please use the format: first_name last_name (John Doe)")
                return False
        
    if len(birthday) != 0:
        try:
            split = birthday.split("-")
            year = int(split[0])
            month = int(split[1])
            day = int(split[2])

            if year > 2023 or year < 1910:
                display_custom_error("INVALID YEAR", "Invalid birth year!")
                return False
                
            if month > 12 or month < 0:
                display_custom_error("INVALID MONTH", "Invalid birth month!")
                return False
                
            if day > 31 or day < 0:
                display_custom_error("INVALID DAY", "Invalid birth day!")
                return False
                
        except Exception as e:
                display_custom_error("INVALID BIRTHDAY", "Invalid birthday format! Please use the format: YYYY-MM-DD")
                return False
            
    if len(str(pin)) != 0:
        try:
            pin = int(pin)
        except:
            display_custom_error(WRONG_DATA_TYPE, "Invalid pin data type! Please use the format: XXXX with ONLY numbers!") 
            return False

        if len(str(pin)) != 4:
            display_custom_error("INVALID PIN", "Invalid pin format! Please use the format: XXXX")       
            return False
            
    if len(email) != 0:
        if "@" in email and ".com" in email:    
            result, success = db.get_email(email)

            if success and result != None:
                display_custom_error(ALREADY_EXISTS, "Email already exists!")      
                return False
        else:
            display_custom_error("INVALID EMAIL", "Invalid email format! Please use the format: example@domain.com")      
            return False
        
    return True



"""

ADMIN UI

"""
class AdminGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CL Banking - ADMIN")
        self.setMinimumSize(960, 540)
        self.setStyleSheet("""

            QWidget {
                background-color: #2D2D2D;
            }

            QLabel {
                font-size: 16px;
                color: #FFFFFF;
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

        welcome_message = QLabel("Welcome CL Admin!")
        welcome_message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        create_button = QPushButton("Create Account")
        create_button.clicked.connect(self.create)

        modify_button = QPushButton("Modify Account")
        modify_button.clicked.connect(self.modify)

        delete_button = QPushButton("Delete Account")
        delete_button.clicked.connect(self.delete)

        layout.addWidget(welcome_message)
        layout.addWidget(create_button)
        layout.addWidget(modify_button)
        layout.addWidget(delete_button)

    def create(self):
        global CREATE_PAGE

        CREATE_PAGE = Create()
        CREATE_PAGE.show()
        self.hide()


    def modify(self):
        global MODIFY_PAGE

        MODIFY_PAGE = Modify()
        MODIFY_PAGE.show()
        self.hide()

    def delete(self):
        global DELETE_PAGE

        DELETE_PAGE = Delete()
        DELETE_PAGE.show()
        self.hide()

class Create(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setFixedSize(400, 400)
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

            QToolButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background-color: #CCCCCC;
            }

            QPushButton:hover {
                background-color: #0061A7;
            }
        ''')

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        

        header = QHBoxLayout()

        title_label = QLabel("Create Account")
        title_label.setFont(QFont("Arial"))
        title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setMargin(0)

        back_button = QToolButton()
        back_button.setIcon(QIcon("C:\\Users\\CJ Lester\\Downloads\\Code Workspace\\Python\\BankingSystem\\Library\\back_arrow.png"))
        size = QSize()
        size.setHeight(35)
        size.setWidth(35)
        back_button.setIconSize(size)
        back_button.clicked.connect(self.back)
        header.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        form_layout = QFormLayout()
        form_layout.addWidget(title_label)
        form_layout.setHorizontalSpacing(10)

        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("John Doe")
        form_layout.addRow(name_label, self.name_input)

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@domain.com")
        form_layout.addRow(email_label, self.email_input)

        passsword_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("example123")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow(passsword_label, self.password_input)

        ssn_label = QLabel("SSN:")
        self.ssn_input = QLineEdit()
        self.ssn_input.setPlaceholderText("XXX-XX-XXXX")
        form_layout.addRow(ssn_label, self.ssn_input)

        birthday_label = QLabel("DOB:")
        self.birthday_input = QLineEdit()
        self.birthday_input.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow(birthday_label, self.birthday_input)

        pin_label = QLabel("PIN:")
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("XXXX")
        form_layout.addRow(pin_label, self.pin_input)

        save_button = QPushButton("Create")
        save_button.clicked.connect(self.save_changes)

        form_layout.addWidget(save_button)

        main_layout.addLayout(form_layout)

    def save_changes(self):

        raw_name = self.name_input.text()
        birthday = self.birthday_input.text()
        email = self.email_input.text()
        pin = self.pin_input.text()
        ssn = self.ssn_input.text()
        password = self.password_input.text()

        valid = check_creation(raw_name, birthday, pin, email, password, ssn)

        if valid:
            raw_name = self.name_input.text()
            raw_name = str.split(raw_name)
            fname = raw_name[0]
            lname = raw_name[1]

            birthday = self.birthday_input.text()
            pin = self.pin_input.text()
            ssn = self.ssn_input.text()
            password = self.password_input.text()

            result, success = db.create_user(f"'{fname}'", f"'{lname}'", f"'{email}'", f"'{password}'", f"'{ssn}'", f"'{birthday}'", f"'{pin}'")

            if success:   
                display_message("Account Creation", "Account Created! \nAccount Number: "+str(result))
                ADMIN_PAGE = Homepage()
                ADMIN_PAGE.show()
                self.hide()
            else:
                display_error(result)


    def back(self):
        global ADMIN_PAGE

        ADMIN_PAGE = AdminGUI()
        ADMIN_PAGE.show()
        self.hide()

def check_creation(name, birthday, pin, email, password, social_security_number):
    # first_name, last_name, email, password, social_security_number, date_of_birth, pin
    # NAME
    try:
            split = name.split(" ")
            fname = split[0]
            lname = split[1]
    except:
            display_message("INVALID NAME", "Invalid name! Please use the format: first_name last_name (John Doe)")
            return False
    
    # EMAIL   
    if "@" in email and ".com" in email:    
        result, success = db.get_email(f"'{email}'")

        if success and result != None:
            display_custom_error(ALREADY_EXISTS, "Email already exists!")      
            return False
    else:
        display_custom_error("INVALID EMAIL", "Invalid email format! Please use the format: example@domain.com")      
        return False
    
    # PASSWORD
    if len(str(password)) < 6:
        display_custom_error("INVALID PASSWORD", "Invalid password! Please make your password at least 6 characters!")     
        return False
    
    # PIN
    try:
        pin = int(pin)
        
        if len(str(pin)) != 4:
            display_custom_error("INVALID PIN", "Invalid pin format! Please use the format: XXXX")       
            return False
    except:
        display_custom_error(WRONG_DATA_TYPE, "Invalid pin data type! Please use the format: XXXX with ONLY numbers!") 
        return False
    
    # DOB
    try:
        split = birthday.split("-")
        year = int(split[0])
        month = int(split[1])
        day = int(split[2])

        if year > 2023 or year < 1910:
            display_custom_error("INVALID YEAR", "Invalid birth year!")
            return False
                
        if month > 12 or month < 0:
            display_custom_error("INVALID MONTH", "Invalid birth month!")
            return False
                
        if day > 31 or day < 0:
            display_custom_error("INVALID DAY", "Invalid birth day!")
            return False
                
    except Exception as e:
                display_custom_error("INVALID BIRTHDAY", "Invalid birthday format! Please use the format: YYYY-MM-DD")
                return False
    
    return True

class Modify(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modify")
        self.setFixedSize(400, 400)
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

            QToolButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background-color: #CCCCCC;
            }

            QPushButton:hover {
                background-color: #0061A7;
            }
        ''')

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        

        header = QHBoxLayout()

        title_label = QLabel("Modify Account")
        title_label.setFont(QFont("Arial"))
        title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setMargin(10)

        back_button = QToolButton()
        back_button.setIcon(QIcon("C:\\Users\\CJ Lester\\Downloads\\Code Workspace\\Python\\BankingSystem\\Library\\back_arrow.png"))
        size = QSize()
        size.setHeight(35)
        size.setWidth(35)
        back_button.setIconSize(size)
        back_button.clicked.connect(self.back)
        header.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        form_layout = QFormLayout()
        form_layout.addWidget(title_label)
        form_layout.setHorizontalSpacing(3)



        account_number = QLabel("Account Number:")
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("XXXXXXXXX")
        form_layout.addRow(account_number, self.account_input)

        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("John Doe")
        form_layout.addRow(name_label, self.name_input)


        birthday_label = QLabel("DOB:")
        self.birthday_input = QLineEdit()
        self.birthday_input.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow(birthday_label, self.birthday_input)

        pin_label = QLabel("PIN:")
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("XXXX")
        form_layout.addRow(pin_label, self.pin_input)

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@domain.com")
        form_layout.addRow(email_label, self.email_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_changes)
        form_layout.addWidget(save_button)

        main_layout.addLayout(form_layout)

    def back(self):
        global ADMIN_PAGE

        ADMIN_PAGE = AdminGUI()
        ADMIN_PAGE.show()
        self.hide()

    def save_changes(self):

        name = self.name_input.text()
        birthday = self.birthday_input.text()
        pin = self.pin_input.text()
        email = self.email_input.text()

        valid = check_information(name, birthday, pin, email)

        if valid:
            global HOME_PAGE

            success = False
            result = "NO CHANGES MADE"

            if len(name) != 0:

                fname = name.split(" ")[0]
                lname = name.split(" ")[1]

                result, success = db.save_to_user(int(self.account_input.text()), "first_name", f"'{fname}'")
                result, success = db.save_to_user(int(self.account_input.text()), "last_name", f"'{lname}'")

            if len(birthday) != 0:
                result, success = db.save_to_user(int(self.account_input.text()), "date_of_birth", f"'{birthday}'")
            if len(str(pin)) != 0:
                result, success = db.save_to_user(int(self.account_input.text()), "pin", pin)
            if len(email) != 0:
                result, success = db.save_to_user(int(self.account_input.text()), "email", f"'{email}'")

            
            if success:   
                display_message("Changes Saved", "Your changes have been saved")
            else:
                display_error(result)

            HOME_PAGE = Homepage()
            HOME_PAGE.show()
            self.hide()

class Delete(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delete")
        self.setFixedSize(400, 200)
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

            QToolButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background-color: #CCCCCC;
            }

            QPushButton:hover {
                background-color: #0061A7;
            }
        ''')

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        

        header = QHBoxLayout()

        title_label = QLabel("Delete Account")
        title_label.setFont(QFont("Arial"))
        title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back_button = QToolButton()
        back_button.setIcon(QIcon("C:\\Users\\CJ Lester\\Downloads\\Code Workspace\\Python\\BankingSystem\\Library\\back_arrow.png"))
        size = QSize()
        size.setHeight(35)
        size.setWidth(35)
        back_button.setIconSize(size)
        back_button.clicked.connect(self.back)
        header.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        form_layout = QFormLayout()
        form_layout.addWidget(title_label)
        form_layout.setHorizontalSpacing(2)

        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Account Number")
        form_layout.addWidget(self.account_input)

        close_account_label = QLabel("")
        self.close_account_button = QPushButton("Close Account")
        self.close_account_button.setStyleSheet("QPushButton { background-color: #E34234; color: #FFFFFF; border-radius: 5px; font-size: 14px; padding: 8px; } QPushButton:hover { background-color: #b82619; }")
        form_layout.addRow(close_account_label, self.close_account_button)
        self.close_account_button.clicked.connect(self.close_account)
        
        main_layout.addLayout(form_layout)

    def back(self):
        global ADMIN_PAGE

        ADMIN_PAGE = AdminGUI()
        ADMIN_PAGE.show()
        self.hide()

    def close_account(self):

        text, boolean = QInputDialog.getText(None, "Pin", "Enter your pin:", echo=QLineEdit.EchoMode.Password)

        if boolean:

            try:
                text = int(text)
            except:
                display_error(WRONG_DATA_TYPE)
                return
                
            p, s = db.get_from_user(int(self.account_input.text()), "pin")

            if s:

                if int(p[0]) == text:
                    pass
                else:
                    display_custom_error("UNAUTHORIZED", "Incorrect pin number!")
                    return
            else:
                display_error(p)
                return 
                
            result, success = db.delete_user(int(self.account_input.text()), text)

            if success:
                global ADMIN_PAGE
                display_success("Account Deleted!")
                ADMIN_PAGE = AdminGUI()
                ADMIN_PAGE.show()
                self.hide()
    