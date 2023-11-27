import csv, os
import copy
import time


class CSV_Reader:
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
    def __init__(self, rank, user_id, data_base):
        self.clearance = rank
        self.advisor = False
        self.database = data_base
        self.id = user_id
        self.username = self.find_username(self.id)

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
        return False

    def find_user(self, user_id):
        for i in self.database.search("persons.csv").table:
            if i["ID"] == str(user_id):
                return i

    def find_username(self, user_id):
        for i in self.database.search("login.csv").table:
            if i["ID"] == str(user_id):
                return i["username"]

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
                self.database.search(table).update(index, key, data)
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
                    if (request["Advisor"].split())[0] in self.username:
                        print(f"Project ID: {request['Project ID']}\n"
                              f"Requesting {request['Advisor']}")
                        print()
            elif action == "2":
                print("Select request to confirm.")
                for request in self.database.search("Advisor_request.csv").table:
                    if (request["Advisor"].split()[0]) in self.username:
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
                for project in self.database.search("Projects.csv").table:
                    if str(self.id) in project["Lead"]:
                        print("You already have a project.")
                        return
                if len(self.database.search("Projects.csv").table) is None:
                    project.update({"ID": "0001"})
                else:
                    uid = str(len(self.database.search("Projects.csv").table) + 1)
                    while len(uid) < 4:
                        uid = "0" + uid
                    project.update({"ID": uid})
                title = input("Enter project title: ")
                project.update({"Title": title})
                project.update(({"Lead": f"{self.username} : {self.id}"}))
                project.update({"Member1": "None"})
                project.update({"Member2": "None"})
                project.update({"Advisor": "None"})
                project.update({"Status": "Awaiting revision"})
                project.update({"Details": "first draft"})
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
                    stu_id = input("Enter student ID: ")
                    for member in self.database.search("Projects.csv").table:
                        if stu_id in member["ID"]:
                            print("Student is already in a project.")
                            return
                    for students in self.database.search("persons.csv").table:
                        if stu_id in students["ID"]:
                            member_flag = True
                            break
                    if not member_flag:
                        print("ID is invalid.")
                        return
                    member_flag = False
                    request = {}
                    if len(self.database.search("Projects.csv").table) == 0:
                        print("You do not have a project. Create one first.")
                        return
                    for projects in self.database.search("Projects.csv").table:
                        if str(self.id) in projects["Lead"]:
                            request.update({"Project ID": projects["ID"]})
                            request.update({"Member": stu_id})
                            request.update({"Response": "Awaiting response"})
                            request.update({"Date": time.asctime(time.localtime())})
                            self.database.search("member_request.csv").insert([request])
                            print(self.database.search("member_request.csv"))
                            member_flag = True
                            break
                    if not member_flag:
                        print("You do not have a project. Create one first.")
                        return
                elif choice == "2":
                    user_ids = []
                    count = 1
                    buffer = 0
                    print("Showing Accepted requests.")
                    for request in self.database.search("member_request.csv").table:
                        for project in self.database.search("Projects.csv").table:
                            if request["Project ID"] in project["ID"]:
                                if str(self.id) in project["Lead"]:
                                    if request["Response"] == "Awaiting confirmation":
                                        print(f"{count}. "
                                              f"{self.find_user(request['Member'])['first']} "
                                              f"{self.find_user(request['Member'])['last']} "
                                              f"ID: {request['Member']}")
                                        user_ids.append(request['Member'])
                                        request["Response"] = "pending"
                                        count += 1
                                        continue
                                    buffer += 1
                    if count == 1:
                        print("No pending request found.")
                        return
                    print(self.database.search("member_request.csv").table)
                    request = input("Enter a request number to "
                                    "approve or deny: ")
                    while int(request) not in range(count+1):
                        print("Invalid request number.")
                        request = input("Enter a request number to "
                                        "approve or deny: ")
                    response = input("Approve or deny: ")
                    not_full = False
                    for project in self.database.search("Projects.csv").table:
                        if str(self.id) in project["Lead"]:
                            if project["Member1"] == "None":
                                project["Member1"] = (f"{self.find_username(user_ids[int(request)-1])}"
                                                      f" : {user_ids[int(request)-1]}")
                                not_full = True
                                break
                            elif project["Member2"] == "None":
                                project["Member2"] = (f"{self.find_username(user_ids[int(request)-1])}"
                                                      f" : {user_ids[int(request)-1]}")
                                not_full = True
                                break
                    if not not_full:
                        print("The project is full.")
                        return
                    for i in self.database.search("member_request.csv").table:
                        if i["Response"] == "pending":
                            i["Response"] = "Awaiting confirmation"
                    self.database.search("member_request.csv").table[
                        int(request) - 1 + buffer].update({"Response": response})
                    for project in self.database.search("Projects.csv").table:
                        if str(self.id) in project["Lead"]:
                            if project["Member1"] != "None" and project["Member2"] != "None":
                                project["Status"] = "Awaiting advisor"
                    print(self.database.search("member_request.csv").table)
                    print()
                    print(self.database.search("Projects.csv").table)
            elif action == "4":
                print("Updating details. Enter esc to exit.")
                for project in self.database.search("Projects.csv").table:
                    if str(self.id) in project["Lead"]:
                        details = input("Enter details: ")
                        if details == "esc":
                            return
                        project["Details"] = details
                        print(project)
                        return
                print("Project not found have you created one yet?")
            elif action == "5":
                advisor_list = []
                count = 1
                check = False
                for project in self.database.search("Projects.csv").table:
                    if self.id in project["Lead"]:
                        check = True
                if not check:
                    print("You do not have a project. Create one first.")
                    return
                print("List of advisors: ")
                for advisors in self.database.search("persons.csv").table:
                    if advisors["type"] == "faculty":
                        advisor_list.append(advisors)
                        print(f"{count}. {advisors['first']} {advisors['last']}")
                        count += 1
                print("Enter a number from the list to invite an advisor.")
                advisor = input("Enter number: ")
                while int(advisor) not in range(count):
                    print("Advisor is not in the list.")
                    advisor = input("Enter number: ")
                request = {}
                for projects in self.database.search("Projects.csv").table:
                    if str(self.id) in projects["Lead"]:
                        request.update({"Project ID": projects["ID"]})
                        request.update({"Advisor":
                                        f"{advisor_list[int(advisor)-1]['first']} "
                                        f"{advisor_list[int(advisor)-1]['last']}"}
                                       )
                        request.update({"Response": "Awaiting response"})
                        request.update(
                            {"Date": time.asctime(time.localtime())})
                        self.database.search("Advisor_request.csv").insert(
                            [request])
                        print("Request sent")
                        print(self.database.search("Advisor_request.csv"))
            elif action == "6":
                check = False
                for projects in self.database.search("Projects.csv").table:
                    if str(self.id) in projects["Lead"]:
                        check = True
                if not check:
                    print("No project provided aborting.")
                    return
                print("Submitting final project for evaluation.")
                choice = input("Confirm?(yes/no): ")
                while choice != "yes" and choice != "no":
                    print("Invalid choice.")
                    choice = input("Confirm?(yes/no): ")
                if choice == "yes":
                    print("Project submitted.")
                    pass
                    # check proposal.md
                elif choice == "no":
                    print("Aborting.")
                    return
        elif self.clearance == 4:
            if action == "1":
                check = False
                print("Your project invitations.")
                for inv in self.database.search("member_request.csv").table:
                    if str(self.id) == inv["Member"]:
                        for projects in self.database.search("Projects.csv").table:
                            if projects["ID"] == inv['Project ID']:
                                print(f"Project ID: {inv['Project ID']} "
                                      f"Title: {projects['Title']}")
                                check = True
                if not check:
                    print("No invitations.")
            elif action == "2":
                proj_list = []
                print("Eligible projects to join.")
                for inv in self.database.search("member_request.csv").table:
                    if str(self.id) == inv["Member"]:
                        if inv["Response"] == "Awaiting response":
                            print(f"Project ID: {inv['Project ID']}")
                            proj_list.append(inv["Project ID"])
                            continue
                    print("No projects found.")
                    return
                projects = input("Enter project ID (type esc to cancel): ")
                if projects == "esc":
                    return
                while projects not in proj_list:
                    print("Invalid project ID")
                    projects = input("Enter project ID (type esc to cancel): ")
                    if projects == "esc":
                        return
                for inv in self.database.search("member_request.csv").table:
                    if str(self.id) == inv["Member"]:
                        if projects == inv["Project ID"]:
                            inv["Response"] = "Awaiting confirmation"
                print(self.database.search("member_request.csv"))
            elif action == "3":
                print("Become a lead student?")
                answer = input("(yes/no): ")
                while answer != "yes" and answer != "no":
                    print("Invalid choice.")
                    answer = input("(yes/no): ")
                if answer == "yes":
                    for user in self.database.search("persons.csv").table:
                        if user["ID"] == str(self.id):
                            self.clearance = 3
                            user["type"] = "lead"
        elif self.clearance == 5:
            print("Updating details. Enter esc to exit.")
            for project in self.database.search("Projects.csv").table:
                print(self.id)
                print(project["Member1"])
                if (str(self.id) in project["Member1"] or
                        str(self.id) in project['Member2']):
                    details = input("Enter details: ")
                    if details == "esc":
                        return
                    project["Details"] = details
                    print(project)
                    return


if __name__ == "__main__":
    # test cases
    print(CSV_Reader("persons.csv").read())
    print()
    print(Table("persons", CSV_Reader("persons.csv").read()))
    print()
    print(Table("persons", CSV_Reader("persons.csv").read())
          .insert([{'friend': 'joe'}, {'animal': "duck"}]))
    print()
    print(Table("persons", CSV_Reader("persons.csv").read())
          .update(0, "ID", 1))
    db = Database()
    x = Table("persons.csv", CSV_Reader("persons.csv").read())
    db.insert(x)
    y = Table("Advisor_request.csv",
              CSV_Reader("Advisor_request.csv").read())
    db.insert(y)
    z = Table("Projects.csv",
              CSV_Reader("Projects.csv").read())
    db.insert(z)
    a = Table("member_request.csv",
              CSV_Reader("member_request.csv").read())
    db.insert(a)
    b = Table("login.csv", CSV_Reader("login.csv").read())
    db.insert(b)
    clearance = int(input("Enter your clearance: "))
    u1 = User(clearance, '2472659', db)
    u1.manage()

    # table for clearance
    # 1 = admin
    # 2 = faculty
    # 3 = Lead
    # 4 student
    # 5 member
