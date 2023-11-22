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


# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database


# define a funcion called login

def login():
    user = input("Enter username: ")
    password = input("Enter password: ")
    for users in db.search("login.csv").table:
        if user in users["username"]:
            if password in users["password"]:
                return [users["ID"], users["role"]]
    return


# define a function called exit
def exit():
    for tables in db.database:
        keys = tables.table[0].keys()
        myFile = open(f"Modified files/{tables.table_name}" + ".modified", 'w')
        writer = csv.DictWriter(myFile, fieldnames= keys)
        writer.writeheader()
        writer.writerows(tables.table)
        myFile.close()
        myFile = open(f"Modified files/{tables.table_name}" + ".modified", 'r')
        print("The content of the csv file is:")
        print(myFile.read())
        myFile.close()

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

initializing()
session = True
while session:
    val = login()
    while val == None:
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
