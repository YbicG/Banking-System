import database as db
import gui_library
from gui_library import Application
from errors import *

# WINDOWS   
login = gui_library.Login(db.login)

db.print_users()

if __name__ == "__main__":
    login.show()
    Application.exec()
