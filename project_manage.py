import database
import os
import csv


def initializing():
    db = database.Database()
    print("Read files:")
    for files in os.listdir():
        if files.endswith(".csv"):
            data = database.Table(files, database.CsvReader(files).read())
            print(files)
            db.insert(data)
    return db

def login(db):
    user = input("Enter username: ")
    password = input("Enter password: ")
    for users in db.search("login.csv").table:
        if user in users["username"]:
            if password in users["password"]:
                return [users["ID"], users["role"]]
    return


def exit(db):
    for tables in db.database:
        if len(tables.table) != 0:
            keys = tables.table[0].keys()
            myFile = open(tables.table_name, 'w')
            writer = csv.DictWriter(myFile, fieldnames= keys)
            writer.writeheader()
            writer.writerows(tables.table)
            myFile.close()
            myFile = open(tables.table_name, 'r')
            print(f"The content of {tables.table_name} is:")
            print(myFile.read())
            myFile.close()


data_base = initializing()
val = login(data_base)
while val is None:
    print("Username or password is invalid.")
    val = login(data_base)
session = True
while session:
    if val[1] == 'admin':
        user = database.User(1, val[0], data_base)
        session = user.manage()
    elif val[1] == 'student':
        user = database.User(4, val[0], data_base)
        session = user.manage()
    elif val[1] == 'member':
        user = database.User(5, val[0], data_base)
        session = user.manage()
    elif val[1] == 'lead':
        user = database.User(3, val[0], data_base)
        session = user.manage()
    elif val[1] == 'faculty':
        user = database.User(2, val[0], data_base)
        session = user.manage()
    elif val[1] == 'advisor':
        user = database.User(2, val[0], data_base)
        session = user.manage()


exit(data_base)
