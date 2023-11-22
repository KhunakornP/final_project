import csv, os
import copy


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
    def __init__(self, rank, user):
        self.clearance = rank
        self.username = user
        self.advisor = False

    def manage(self):
        print(f"Welcome {self.username} here are your available actions.")
        self.actions()
        action = input("Enter action: ")
        while action != "0":
            self.actions()
            action = input("Enter action: ")

    def actions(self):
        if self.clearance == 1:
            print("1. Update the database.")
        if self.clearance == 2:
            print("1. See advisor requests.")
            print("2. Respond to requests.")
            print("3. See project details.")
            print("4. Evaluate Projects.")
            if self.advisor:
                print("5. Approve project")
        if self.clearance == 3:
            print("1. Create project.")
            print("2. Find members.")
            print("3. Send invitation.")
            print("4. Modify project details.")
            print("5. Request advisor.")
            print("6. Submit project for approval.")
        if self.clearance == 4:
            print("1. See project invitations.")
            print("2. Respond to invitations.")
            print("3. Elevate to lead student.")
        if self.clearance == 5:
            print("1. Modify project details.")
        print("Enter 0 to exit.")

if __name__ == "__main__":
    # test cases
    print(csv_Reader("persons.csv").read())
    print()
    print(Table("persons", csv_Reader("persons.csv").read()))
    print()
    print(Table("persons", csv_Reader("persons.csv").read())
          .insert([{'friend': 'joe'}, {'animal' : "duck"}]))
    print()
    print(Table("persons", csv_Reader("persons.csv").read())
          .update(0,"ID", 1))
    u1 = User(1, "joe")
    u1.manage()
    # table for clearance
    # 1 = admin
    # 2 = faculty
    # 3 = Lead
    # 4 student
    # 5 member