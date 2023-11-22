import csv, os
import copy
import time


class csv_Reader:
    def __init__(self, name):
        self.data = []
        self.name = name

    def read(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        with open(os.path.join(__location__, self.name)) as f:
            rows = csv.DictReader(f)
            for row in rows:
                self.data.append(dict(row))
        return self.data


class Database:
    def __init__(self):
        self.database = []

    def insert(self, data):
        self.database.append(data)

    def search(self, name):
        for table in self.database:
            if table.table_name == name:
                return table
        return

# add in code for a Table class
class Table:
    def __init__(self, name, table):
        self.table_name = name
        self.table = table

    def insert(self, data):
        for item in data:
            self.table.append(item)
        return self.table

    def join(self, other_table, common_key):
        joined_table = Table(
            self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def update(self, index, key, value):
        self.table[index][key] = value
        return self.table

    def __str__(self):
        return self.table_name + ':' + str(self.table)


class User:
    def __init__(self, rank, user, db):
        self.clearance = rank
        self.username = user
        self.advisor = False
        self.database = db
    def manage(self):
        print(f"Welcome {self.username} here are your available actions.")
        self.help()
        action = input("Enter action: ")
        print()
        while action != "0":
            self.actions(action)
            self.help()
            action = input("Enter action: ")
            print()

    def help(self):
        if self.clearance == 1:
            print("1. Update the database.")
        elif self.clearance == 2:
            print("1. See advisor requests.")
            print("2. Respond to requests.")
            print("3. See project details.")
            print("4. Evaluate Projects.")
            if self.advisor:
                print("5. Approve project")
        elif self.clearance == 3:
            print("1. Create project.")
            print("2. Find members.")
            print("3. Send invitation.")
            print("4. Modify project details.")
            print("5. Request advisor.")
            print("6. Submit project for approval.")
        elif self.clearance == 4:
            print("1. See project invitations.")
            print("2. Respond to invitations.")
            print("3. Elevate to lead student.")
        elif self.clearance == 5:
            print("1. Modify project details.")
        print("Enter 0 to exit.")

    def actions(self, action):
        if self.clearance == 1:
            print("Updating database to quit enter esc: ")
            print("All Tables: ")
            for tables in self.database.database:
                print(tables.table_name)
            table = input("Enter table to update: ")
            index = int(input("Enter index: "))
            key = input("Enter key: ")
            data = input("Enter data: ")
            print()
            while table != "esc" and key != "esc" and data != "esc":
                self.database.search(table).update(index, key,data)
                table = input("Enter table to update: ")
                index = int(input("Enter index: "))
                key = input("Enter key: ")
                data = input("Enter data: ")
                print()
            print(self.database.search(table))
        elif self.clearance == 2:
            if action == "1":
                for request in self.database.search("Advisor_request.csv").table:
                    print("Your current requests.")
                    if request["Advisor"] == self.username:
                        print(f"Project ID: {request['Project ID']}\n"
                              f"Requesting {request['Advisor']}")
                        print()
            elif action == "2":
                print("Select request to confirm.")
                for request in self.database.search("Advisor_request.csv").table:
                    if request["Advisor"] == self.username:
                        print(f"Project ID: {request['Project ID']}")
                project_id = input("Enter id: ")
                response = input("Enter response: ")
                for request in self.database.search("Advisor_request.csv").table:
                    if request["Project ID"] == project_id:
                        request["Response"] = response
                        date = time.localtime()
                        request["Date of response"] = time.asctime(time.localtime())
                        print(self.database.search("Advisor_request.csv"))


if __name__ == "__main__":
    # test cases
    # print(csv_Reader("persons.csv").read())
    # print()
    # print(Table("persons", csv_Reader("persons.csv").read()))
    # print()
    # print(Table("persons", csv_Reader("persons.csv").read())
    #       .insert([{'friend': 'joe'}, {'animal' : "duck"}]))
    # print()
    # print(Table("persons", csv_Reader("persons.csv").read())
    #       .update(0,"ID", 1))
    db = Database()
    x =Table("persons", csv_Reader("persons.csv").read())
    db.insert(x)
    x = Table("Advisor_request.csv", csv_Reader("Advisor_request.csv").read())
    db.insert(x)
    u1 = User(2, "Karim.B",db)
    u1.manage()

    # table for clearance
    # 1 = admin
    # 2 = faculty
    # 3 = Lead
    # 4 student
    # 5 member