from getpass import getpass
from mysql.connector import connect, Error as error
import random
from config import config

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
            social_security_number VARCHAR(100),
            date_of_birth DATE,
            account_number INT,
            pin INT
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
    except error as e:
        print(e)

# Making a new account
def create_user(first_name, last_name, email, social_security_number, date_of_birth, pin):

    # Generating a completely unique UID for an account number

    uid = random.randint(100000000, 999999999)

    val, success = get_from_user(uid, "first_name")

    while success != True:

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

        # Formating the query

        query = """
        INSERT INTO user_information(first_name, last_name, email, social_security_number, date_of_birth, account_number, pin)
        VALUES
            ({}, {}, {}, {}, {}, {}, {})
        """.format(first_name, last_name, email, social_security_number, date_of_birth, uid, pin)   

        # Executing the query

        with connection.cursor() as cursor:
            
            cursor.execute(query)
            connection.commit()

            # Returning value of query and success boolean  

            return uid, True
        
    except error as e:

        # Returning empty value of query and fail boolean

        print(e)
        return e, False

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

        value = cursor.fetchone()

        if value == None:
            return [], False
        
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
