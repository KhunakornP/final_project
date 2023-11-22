import database
import os
import csv


def initializing():
    global db
    db = database.Database()
    for files in os.listdir():
        if files.endswith(".csv"):
            data = database.Table(files, database.csv_Reader(files).read())
            print(data)
            db.insert(data)

def login():
    user = input("Enter username: ")
    password = input("Enter password: ")
    for users in db.search("login.csv").table:
        if user in users["username"]:
            if password in users["password"]:
                return [users["ID"], users["role"]]
    return

def exit():
    for tables in db.database:
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


initializing()
session = True
while session:
    val = login()
    while val is None:
        print("Username or password is invalid.")
        val = login()
    if val[1] == 'admin':
        pass
    elif val[1] == 'student':
        pass
    elif val[1] == 'member':
        pass
    elif val[1] == 'lead':
        pass
    elif val[1] == 'faculty':
        pass
    elif val[1] == 'advisor':
        pass


# once everyhthing is done, make a call to the exit function
exit()
