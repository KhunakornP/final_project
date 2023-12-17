"""
Runs the program
"""
import os
import csv
import database


def initializing():
    """
    Initializes the program
    """
    db = database.Database()
    for files in os.listdir():
        if files.endswith(".csv"):
            data = database.Table(files, database.CsvReader(files).read())
            db.insert(data)
    return db


def login(db):
    """
    Log in the user. If the username and password match
    log in the user. Else ask the user for a new
    username and password.
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    for users in db.search("login.csv").table:
        if username in users["username"]:
            if password in users["password"]:
                return [users["ID"], users["role"]]
    return None


def exit(db):
    """
    Exits the program and write all .csv files in the database.
    """
    for tables in db.database:
        if len(tables.table) != 0:
            keys = tables.table[0].keys()
            my_file = open(tables.table_name, 'w')
            writer = csv.DictWriter(my_file, fieldnames= keys)
            writer.writeheader()
            writer.writerows(tables.table)
            my_file.close()


data_base = initializing()
val = login(data_base)
while val is None:
    print("Username or password is invalid.")
    val = login(data_base)
SESSION = True
while SESSION:
    if val[1] == 'admin':
        user = database.User(1, val[0], data_base)
        SESSION = user.manage()
    elif val[1] == 'student':
        user = database.User(4, val[0], data_base)
        SESSION = user.manage()
    elif val[1] == 'member':
        user = database.User(5, val[0], data_base)
        SESSION = user.manage()
    elif val[1] == 'lead':
        user = database.User(3, val[0], data_base)
        SESSION = user.manage()
    elif val[1] == 'faculty':
        user = database.User(2, val[0], data_base)
        SESSION = user.manage()
    elif val[1] == 'advisor':
        user = database.User(2, val[0], data_base)
        SESSION = user.manage()


exit(data_base)
