import random
import os
import hashlib
import errors
from mysql.connector import connect, Error as error
from config import config


# Hashing of passwords and private information

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

# For creating a table to use for DB, not using anymore
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
            balance INT,
            pin INT,
            p_salt VARCHAR(100),
            s_salt VARCHAR(100)
           
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
    except error as e:
        print(e)

# Making a new account
def create_user(first_name, last_name, email, password, social_security_number, date_of_birth, pin):

    #Checking if email already there

    return_value, user_found = get_email(email)

    if user_found and return_value != None:
        print(errors.ALREADY_EXISTS)
        return errors.ALREADY_EXISTS, False

    # Generating a completely unique UID for an account number

    uid = random.randint(100000000, 999999999)

    val, success = get_from_user(uid, "first_name")

    while success == True:

        val, success = get_from_user(uid, "first_name")

        uid = random.randint(100000000, 999999999)  

    try:

        # Setting up a connection

        connection = connect(
            host = config["Host"],
            user = config["Username"],
            password= config["Password"],
            database="users"
        )

        # Encrypting password, social security number

        hashed_password, p_salt = hash_str(password)
        hashed_social_security_number, s_salt = hash_str(social_security_number)

        # Formating the query

        query = """
        INSERT INTO user_information(first_name, last_name, email, password, social_security_number, date_of_birth, account_number, balance, pin, p_salt, s_salt)
        VALUES
            ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
        """.format(first_name, last_name, email, f"'{hashed_password}'", f"'{hashed_social_security_number}'", date_of_birth, uid, 0, pin, "\"{}\"".format(p_salt), "\"{}\"".format(s_salt))   

        # Executing the query

        with connection.cursor() as cursor:
            
            cursor.execute(query)
            connection.commit()

            # Returning value of query and success boolean  

            return uid, True
        
    except error as e:

        # Returning empty value of query and fail boolean

        print(e)
        return errors.CLIENT_DENIED, False

# Saving a new value to an account's variable
def save_to_user(account_number, information_to_change, value):

    try:

        # Setting up a connection

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        # Formating the query

        query = """
        UPDATE
            user_information
        SET
            {info} = {val}
        WHERE
            account_number = {acc_num}
        """.format(acc_num=account_number, info=information_to_change, val=value)

        # Executing the query

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        # Success boolean  

        return None, True
        
    except error as e:

        # Fail boolean  

        print(e)
        return e, False
    
# Getting a value from an account variable
def get_from_user(account_number, information_to_get):

    try:

        # Setting up a connection

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        # Formating the query

        query = """
        SELECT {info}
        FROM user_information
        WHERE account_number = {acc_num}
        """.format(acc_num=account_number, info=information_to_get)

        # Executing the query

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        # Fetching the values

        value = cursor.fetchall()

        if value == []:
            return None, False
        
        return_val = value[0]

        # Returning value of query and success boolean  

        return return_val, True
        
    except error as e:

        # Returning empty value of query and fail boolean

        print(e)
        return e, False

# Printing every user
def print_users():

    try:

        # Setting up a connection

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        # Formating the query

        query = """
        SELECT *
        FROM user_information
        """

        # Executing the query

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        # Receiving all users and printing values

        for i in cursor.fetchall():
            print(i)

    except error as e:
        print(e)

# Checking if email exists
def get_email(email):

    try:

        # Setting up a connection

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        # Formating the query

        query = """
        SELECT *
        FROM user_information
        WHERE email = {email}
        """.format(email=email)

        # Executing the query

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        # Fetching the values

        value = cursor.fetchone()

        if value == None:
            return None, False
        
        return_val = value[0]

        # Returning value of query and success boolean  

        return return_val, True
        
    except error as e:

        # Returning empty value of query and fail boolean

        print(e)
        return e, False
    


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


# Login function  
def login(email, password):

    try:

        # Setting up a connection

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        # Formating the query
        
        query = """
        SELECT password, p_salt, account_number
        FROM user_information
        WHERE email = {email}
        """.format(email=email)

        # Executing the query

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()
        
        # Fetching the values

        value = cursor.fetchall()

        if value == []:
            return errors.NOT_FOUND, False
        
        value = value[0]
        
        decoded_salt = sep_bytes(value[1]).encode()
        # Encrypting password
        
        hashed_password, p_salt = hash_str_with_salt(password, decoded_salt)

        # Returning account number and success boolean if password is right

        account_number = value[2] 

        if hashed_password == value[0]:
            return account_number, True
        else:
            return errors.CLIENT_DENIED, False
        
    except error as e:

        # Returning empty value of query and fail boolean

        print(e)
        return e, False
    
def withdraw(account_number, value):

    try:

        # Setting up a connection

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        # Getting current balance

        balance, sucesss = get_from_user(account_number, "balance")

        if not sucesss:
            return errors.INVALID_PROTOCOL, False
        else:
            if balance[0] >= value:
                value = balance[0] - value
                
                print("Value: ", value)

            else:
                return errors.NOT_ENOUGH_FUNDS, False
        
        # Formating the query
        query = """
        UPDATE
            user_information
        SET
            balance = {val}
        WHERE
            account_number = {acc_num}
        """.format(acc_num=account_number, val=value)

        # Executing the query

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        # Success boolean  

        return None, True
        
    except error as e:

        # Fail boolean  

        print(e)
        return e, False
    
def deposit(account_number, value):

    try:

        # Setting up a connection

        connection = connect(
                host = config["Host"],
                user = config["Username"],
                password= config["Password"],
                database="users"
            )
        
        # Getting current balance

        balance, sucesss = get_from_user(account_number, "balance")

        if not sucesss:
            return errors.INVALID_PROTOCOL, False
        else:
            value = balance[0] + value
        
        # Formating the query
        query = """
        UPDATE
            user_information
        SET
            balance = {val}
        WHERE
            account_number = {acc_num}
        """.format(acc_num=account_number, val=value)

        # Executing the query

        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        connection.commit()

        # Success boolean  

        return value, True
        
    except error as e:

        # Fail boolean  

        print(e)
        return e, False