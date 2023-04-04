import database as db
from errors import *

"""
When typing strings for the functions you have to use \" \" or ' '  to make SQL know it is a string.

Examples:

db.login("\"johnnyappleseed@gmail.com\"", "\"johnnyappleseed\"") | This will work

----------------

db.login("'johnnyappleseed@gmail.com'", "'johnnyappleseed'") | This will work work

----------------

db.login("johnnyappleseed@gmail.com", "johnnyappleseed") | This will not work
"""

db.print_users()

account_number, success = db.login("\"lllexander21911@gmail.com\"", "\"this_will_not_work\"")

print("Account Number: ", account_number, "\nLogged in sucessfully: ", success)