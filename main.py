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


db.create_user("'Johnny'", "'Appleseed'", "'johnnyapple@example.com'", "'JohnApple64@#&!'", "'981-18-1989'", "'1982-01-25'", 2246)

db.print_users()

account_number, success = db.login("'johnnyapple@example.com'", "'JohnApple64@#&!'")

print("Account Number: ", account_number, "\nLogged in sucessfully: ", success)


result, success = db.withdraw(account_number, 0)

if result == NOT_ENOUGH_FUNDS:
    print("You don't have enough money!")

print("Result: ", result, "\nSucess: ", success)

result, success = db.deposit(account_number, 1000)

print("Result: ", result, "\nSucess: ", success)