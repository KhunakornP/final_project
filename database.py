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
    def __init__(self, rank, user, db, ID):
        self.clearance = rank
        self.username = user
        self.advisor = False
        self.database = db
        self.id = ID

    def manage(self):
        print(f"Welcome {self.username} here are your available actions.")
        self.help()
        action = input("Enter action: ")
        print()
        while action != "0":
            self.actions(action)
            print()
            self.help()
            action = input("Enter action: ")

    def find_user(self, ID):
        for i in self.database.search("persons.csv").table:
            if i["ID"] == str(ID):
                return i

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
            print("3. Invite/add students to the project")
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
                        request["Date of response"] = time.asctime(time.localtime())
                        print(self.database.search("Advisor_request.csv"))
            elif action == "3":
                print("List of projects:")
                for projects in self.database.search("Projects.csv").table:
                    print(projects)
            elif action == "4":
                pass
            # evaluation will be implemented in the future
        elif self.clearance == 3:
            project = {}
            if action == "1":
                if len(self.database.search("Projects.csv").table) is None:
                    project.update({"ID" : "0001"})
                else:
                    uid = str(len(self.database.search("Projects.csv").table) + 1)
                    while len(uid) < 4:
                        uid = "0" + uid
                    project.update({"ID": uid})
                title = input("Enter project title: ")
                project.update({"Title": title})
                project.update(({"Lead": f"{self.username} : {self.id}"}))
                project.update({"Member 1": "None"})
                project.update({"Member 2": "None"})
                project.update({"Advisor": "None"})
                project.update({"Status": "Awaiting members"})
                self.database.search("Projects.csv").insert([project])
                print(self.database.search("Projects.csv"))
            elif action == "2":
                print("Showing students without a group.")
                for students in self.database.search("persons.csv").table:
                    if students["ID"] not in self.database.search("Projects.csv").table:
                        if students["type"] == "student":
                            print(f"Name: {students['first']} "
                                  f"{students['last']} ID: {students['ID']}")
            elif action == "3":
                choice = input("1. Invite students\n2. View accepted "
                               "requests\nEnter choice: ")
                print()
                if choice == "1":
                    member_flag = False
                    print("Inviting students to project.")
                    ID = input("Enter student ID: ")
                    for member in self.database.search("Projects.csv").table:
                        if ID in member["ID"]:
                            print("Student is already in a project.")
                            return
                    for students in self.database.search("persons.csv").table:
                        if ID in students["ID"]:
                            member_flag = True
                            break
                    if not member_flag:
                        print("ID is invalid.")
                        return
                    request = {}
                    if len(self.database.search("Projects.csv").table) == 0:
                        print("You do not have a project. Create one first.")
                        return
                    for projects in self.database.search("Projects.csv").table:
                        if str(self.id) in projects["Lead"]:
                            request.update({"Project ID": projects["ID"]})
                            request.update({"Member": ID})
                            request.update({"Response": "Awaiting response"})
                            request.update({"Date": time.asctime(time.localtime())})
                            self.database.search("member_request.csv").insert([request])
                            print(self.database.search("member_request.csv"))
                            break
                        print("You do not have a project. Create 1 first.")
                        return
                elif choice == "2":
                    count = 1
                    print("Showing Accepted requests.")
                    for request in self.database.search("member_request.csv").table:
                        for project in self.database.search("Projects.csv").table:
                            if request["Project ID"] in project["ID"]:
                                if str(self.id) in project["Lead"]:
                                    print(f"{count}. "
                                          f"{self.find_user(request['Member'])['first']} "
                                          f"{self.find_user(request['Member'])['last']} "
                                          f"ID: {request['Member']}")
                                    count += 1
                    if count == 1:
                        print("No pending request found.")
                        return
                    request = input("Enter a request number to approve or"
                                    "deny: ")
                    while int(request) not in range(count+1):
                        print("Invalid request number.")
                        request = input("Enter a request number to approve or"
                                        "deny: ")
                    response = input("Approve or deny: ")
                    self.database.search("member_request.csv").table[
                        int(request) - 1].update({"Response": response})
                    print(self.database.search("member_request.csv").table)







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
    x =Table("persons.csv", csv_Reader("persons.csv").read())
    db.insert(x)
    y = Table("Advisor_request.csv", csv_Reader("Advisor_request.csv").read())
    db.insert(y)
    z = Table("Projects.csv", csv_Reader("Projects.csv").read())
    db.insert(z)
    a = Table("member_request.csv", csv_Reader("member_request.csv").read())
    db.insert(a)
    u1 = User(3, "Karim.B",db, '2472659')
    u1.manage()

    # table for clearance
    # 1 = admin
    # 2 = faculty
    # 3 = Lead
    # 4 student
    # 5 member