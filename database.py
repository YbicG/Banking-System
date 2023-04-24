import random
import os
import hashlib
from Types import errors, bank_admins
from mysql.connector import Error, connect
from Cfg.config import config

# ENCRYPTION FUNCTIONS
def hash_str(string: str):

    salt = os.urandom(10)
    salt = salt.hex()
    salt = salt.encode()

    hash_digest = hashlib.pbkdf2_hmac('sha256', string.encode(), salt, 10000)
    hash = hash_digest.hex()

    return hash, salt

def hash_str_with_salt(string: str, salt):
    
    hash_digest = hashlib.pbkdf2_hmac('sha256', string.encode(), salt, 10000)
    hash = hash_digest.hex()

    return hash, salt

def sep_bytes(string: str):

    split = string.split("b'")

    if len(split) > 2:
        split = split[1]+"b'"
        split = split.split("'")
        split = split[0]
    else:
        split = split[1].split("'")
        split = split[0]

    return split
# END OF ENCRYPTION FUNCTIONS

# CREATION FUNCTIONS
def create_table():

    try:
        connection = connect(
            host = config["Host"],
            user = config["Username"],
            password= config["Password"],
            database="users"
        )
        query = """
        CREATE TABLE user_information(
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(100),
            password VARCHAR(100),
            social_security_number VARCHAR(100),
            date_of_birth DATE,
            account_number INT,
            balance FLOAT(255, 2),
            pin INT,
            p_salt VARCHAR(100),
            s_salt VARCHAR(100)
           
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(query)

    except Error as e:
        print(e)

def create_user(first_name, last_name, email, password, social_security_number, date_of_birth, pin):

    return_value, user_found = get_email(email)

    if user_found and return_value != None:
        print(errors.ALREADY_EXISTS)
        return errors.ALREADY_EXISTS, False

    uid = random.randint(100000000, 999999999)

    val, success = get_from_user(uid, "first_name")

    while success == True:

        val, success = get_from_user(uid, "first_name")

        uid = random.randint(100000000, 999999999)  

    try:

        connection = connect(
            host = config["Host"],
            user = config["Username"],
            password= config["Password"],
            database="users"
        )

        hashed_password, p_salt = hash_str(password)
        hashed_social_security_number, s_salt = hash_str(social_security_number)

        query = """
        INSERT INTO user_information(first_name, last_name, email, password, social_security_number, date_of_birth, account_number, balance, pin, p_salt, s_salt)
        VALUES
            ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
        """.format(first_name, last_name, email, f"'{hashed_password}'", f"'{hashed_social_security_number}'", date_of_birth, uid, 0.00, pin, "\"{}\"".format(p_salt), "\"{}\"".format(s_salt))   

        with connection.cursor() as cursor:
            
            cursor.execute(query)
            connection.commit()

            return uid, True
        
    except Error as e:

        print(e)
        return errors.CLIENT_DENIED, False
# END OF CREATION FUNCTIONS

# USER HANDLING FUNCTIONS
def save_to_user(account_number, information_to_change, value):

    try:

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        query = """
        UPDATE
            user_information
        SET
            {info} = {val}
        WHERE
            account_number = {acc_num}
        """.format(acc_num=account_number, info=information_to_change, val=value)

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        return None, True
        
    except Error as e:

        print(e)
        return errors.CLIENT_DENIED, False

def get_from_user(account_number, information_to_get):

    try:

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
        )

        query = """
        SELECT {info}
        FROM user_information
        WHERE account_number = {acc_num}
        """.format(acc_num=account_number, info=information_to_get)

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        value = cursor.fetchall()

        if value == []:
            return None, False
        
        return_val = value[0]

        return return_val, True
        
    except Error as e:

        print(e)
        return errors.CLIENT_DENIED, False
# END OF USER HANDLING FUNCTIONS

# USER VERIFICATION FUNCTIONS
def get_email(email):

    try:

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )

        query = """
        SELECT *
        FROM user_information
        WHERE email = {email}
        """.format(email=email)

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        value = cursor.fetchone()

        if value == None:
            return None, False
        
        return_val = value[0]

        return return_val, True
        
    except Error as e:

        print(e)
        return errors.CLIENT_DENIED, False

def login(email, password):

    if bank_admins.administrators.get(email):
        if bank_admins.administrators[email]["password"] == password:
            return bank_admins.BANK_ADMIN, True
        
    try:

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        query = """
        SELECT password, p_salt, account_number
        FROM user_information
        WHERE email = {email}
        """.format(email=email)

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        value = cursor.fetchall()

        if value == []:
            return errors.NOT_FOUND, False
        
        value = value[0]
        
        decoded_salt = sep_bytes(value[1]).encode()

        hashed_password, p_salt = hash_str_with_salt(password, decoded_salt)

        account_number = value[2] 

        if hashed_password == value[0]:
            return account_number, True
        else:
            return errors.INVALID_PROTOCOL, False
        
    except Error as e:

        print(e)
        return errors.CLIENT_DENIED, False
# END OF USER VERIFICATION FUNCTIONS

# BALANCE HANDLING FUNCTIONS
def withdraw(account_number, value):

    try:

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        balance, sucesss = get_from_user(account_number, "balance")

        if not sucesss:
            return errors.NOT_FOUND, False
        else:
            if balance[0] >= value:
                value = float(balance[0]) - value
                
                print("Value: ", value)

            else:
                return errors.NOT_ENOUGH_FUNDS, False
        
        query = """
        UPDATE
            user_information
        SET
            balance = {val}
        WHERE
            account_number = {acc_num}
        """.format(acc_num=account_number, val=value)

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        return None, True
        
    except Error as e:

        print(e)
        return errors.CLIENT_DENIED, False
    
def deposit(account_number, value):

    try:

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        

        balance, sucesss = get_from_user(account_number, "balance")

        if not sucesss:
            return errors.NOT_FOUND, False
        else:
            value = float(balance[0]) + value
        
        query = """
        UPDATE
            user_information
        SET
            balance = {val}
        WHERE
            account_number = {acc_num}
        """.format(acc_num=account_number, val=value)


        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        return value, True
        
    except Error as e: 

        print(e)
        return errors.CLIENT_DENIED, False
# END OF BALANCE HANDLING FUNCITONS

# DELETION FUNCTIONS  
def delete_user(account_number, pin):  

    try:


        connection = connect(
            host = config["Host"],
            user = config["Username"],
            password= config["Password"],
            database="users"
        )


        query = f"""
        DELETE FROM user_information

        WHERE
            account_number = {account_number} AND pin = {pin}
            
        """

        with connection.cursor() as cursor:
            
            cursor.execute(query)
            connection.commit()

            res, success = get_from_user(account_number, "*")

            if success and res != None:
                return errors.NOT_FOUND, True
            else:
                return "DELETED", True
        
    except Error as e:

        print(e)
        return errors.CLIENT_DENIED, False
# END OF DELETION FUNCTIONS

# EXTRA FUNCTIONS
def print_users():

    try:

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )

        query = """
        SELECT *
        FROM user_information
        """

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        for i in cursor.fetchall():
            print(i)

    except Error as e:
        print(e)
# END OF EXTRA FUNCTIONS