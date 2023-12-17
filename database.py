import csv, os
import copy
import time


class CsvReader:
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

    def update_table(self, id_value, key, value):
        for data in self.table:
            if data["ID"] == str(id_value):
                data[key] = value
                return data
        return

    def update_dict(self, id_value):
        for data in self.table:
            if data["ID"] == str(id_value):
                for keys in data.keys():
                    data[keys] = input(f"Enter new {keys}: ")
                return data
        return

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
        self.check_advisor()
        if self.finish_project():
            self.clearance = 0
        print(f"Welcome {self.username} here are your available actions.")
        self.help()
        action = input("Enter action: ")
        while action != "0":
            print()
            self.actions(action)
            print()
            self.help()
            action = input("Enter action: ")
        return False

    def check_advisor(self):
        for advisors in self.database.search("Projects.csv").table:
            if advisors["Advisor"] == str(self.id):
                self.advisor = True

    def finish_project(self):
        for projects in self.database.search("Projects.csv").table:
            members = [projects['Lead'], projects['Member1'],
                       projects['Member2']]
            if self.id in members:
                if projects["Status"] == "Finished":
                    print("You have finished your project")
                    print(f"Your project details:\n"
                          f"Title: {projects['Title']} ID: {projects['ID']}")
                    print(f"Lead: {self.find_username(projects['Lead'])}")
                    member1 = self.find_username(projects['Member1'])
                    member2 = self.find_username(projects['Member2'])
                    if member1 is not None:
                        print(f"Member(s): {member1}"
                              f"{'' if member2 is None else ', ' + member2}")
                    print(f"Advisor: {projects['Advisor']}\n"
                          f"Status: {projects['Status']}\n"
                          f"Details: {projects['Details']}")
                    return True
        return False

    def read_project(self):
        for projects in self.database.search("Projects.csv").table:
            members = [projects['Lead'], projects['Member1'],
                       projects['Member2']]
            if self.id in members:
                print(f"Your project details:\n"
                      f"Title: {projects['Title']} ID: {projects['ID']}")
                print(f"Lead: {self.find_username(projects['Lead'])}")
                member1 = self.find_username(projects['Member1'])
                member2 = self.find_username(projects['Member2'])
                if member1 is not None:
                    print(f"Member(s): {member1}"
                          f"{'' if member2 is None else ', ' + member2}")
                print(f"Advisor: {self.find_username(projects['Advisor'])}\n"
                      f"Status: {projects['Status']}\n"
                      f"Details: {projects['Details']}")
                return True
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
            print("1. Update a value.")
            print("2. Update a dictionary.")
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
            if action == "1":
                print("Updating database to quit enter esc: ")
                while True:
                    print("All Tables: ")
                    for tables in self.database.database:
                        print(tables.table_name)
                    print()
                    table = input("Enter table to update: ")
                    if table == "esc":
                        break
                    id_value = input("Enter id: ")
                    if id_value == "esc":
                        break
                    while not id_value.isdigit():
                        print("id is not an int")
                        id_value = input("Enter id: ")
                        if id_value == "esc":
                            break
                    key = input("Enter key: ")
                    if key == "esc":
                        break
                    data = input("Enter data: ")
                    if data == "esc":
                        break
                    print()
                    result \
                        = (self.database.
                           search(table).update_table(id_value, key, data))
                    print(result)
            elif action == "2":
                print("Updating database to quit enter esc: ")
                while True:
                    print("All Tables: ")
                    for tables in self.database.database:
                        print(tables.table_name)
                    print()
                    table = input("Enter table to update: ")
                    if table == "esc":
                        break
                    id_value = input("Enter id to update: ")
                    result = self.database.search(
                        table).update_dict(id_value)
                    print(result)
        elif self.clearance == 2:
            if action == "1":
                if len(self.database.search("Advisor_request.csv").table) < 1:
                    print("No requests found.")
                    return
                for request in (
                        self.database.search("Advisor_request.csv").table):
                    print("Your current requests.")
                    if (request["Advisor"].split())[0] in self.username:
                        print(f"Project ID: {request['ID']}\n"
                              f"Requesting {request['Advisor']}")
                        print()
                    else:
                        print("No requests found.")
            elif action == "2":
                if len(self.database.search("Advisor_request.csv").table) < 1:
                    print("No requests found.")
                    return
                print("Select request to confirm.")
                ids = []
                for request in (
                        self.database.search("Advisor_request.csv").table):
                    if (request["Advisor"].split()[0]) in self.username:
                        print(f"Project ID: {request['ID']}")
                        ids.append(request["ID"])
                    else:
                        print("No requests found.")
                        return
                project_id = input("Enter id: ")
                while project_id not in ids:
                    print("Invalid ID")
                    project_id = input("Enter id: ")
                response = input("Enter response (approve/deny): ")
                for request in (
                        self.database.search("Advisor_request.csv").table):
                    if request["ID"] == project_id:
                        request["Response"] = response
                        request["Date of response"] \
                            = time.asctime(time.localtime())
                        print(self.database.search("Advisor_request.csv"))
                if response == "approve":
                    self.database.search(
                        "persons.csv").update_table(self.id, "type", "advisor")
                    self.database.search(
                        "login.csv").update_table(self.id, "role", "advisor")
                    self.advisor = True
                    for projects in self.database.search("Projects.csv").table:
                        if projects["ID"] == project_id:
                            projects["Advisor"] = self.id
            elif action == "3":
                print("List of projects:")
                if len(self.database.search("Projects.csv").table) == 0:
                    print("No projects found.")
                for projects in self.database.search("Projects.csv").table:
                    print(f'ID: {projects["ID"]} Title: {projects["Title"]}')
                    print(f"Lead: {self.find_username(projects['Lead'])}")
                    member1 = self.find_username(projects['Member1'])
                    member2 = self.find_username(projects['Member2'])
                    if member1 is not None:
                        print(f"Member(s): {member1}"
                              f"{'' if member2 is None else ', ' + member2}")
                    print(f"Status: {projects['Status']}")
            elif action == "4":
                advisor = False
                for items in self.database.search("evaluation.csv").table:
                    if items["evaluators"] == str(self.id):
                        proj_id = items["ID"]
                        evaluation = items
                        advisor = True
                        break
                if advisor:
                    advisor_list = []
                    count = 1
                    print("Showing faculty members")
                    for advisors in self.database.search("persons.csv").table:
                        if advisors["type"] in ["faculty", 'advisor']:
                            if advisors["ID"] != self.id:
                                print(f"{count}. {advisors['first']} "
                                      f"{advisors['last']}")
                                advisor_list.append(advisors)
                                count += 1
                    num = input("Enter the number of advisors"
                                "(esc to cancel): ")
                    if num == "esc":
                        return
                    while not 3 <= int(num) <= len(advisor_list):
                        print("Invalid amount.")
                        num = input("Enter the number of advisors"
                                    "(esc to cancel): ")
                        if num == "esc":
                            return
                    inv = 1
                    inv_list = [self.id]
                    print("Enter a number from the list to invite"
                          " an advisor.")
                    advisor = input("Enter number: ")
                    while int(advisor) not in range(count + 1):
                        print("Advisor is not in the list.")
                        advisor = input("Enter number: ")
                    inv_list.append(advisor_list[int(advisor) - 1]["ID"])
                    advisor_list.pop(int(advisor) - 1)
                    while inv != int(num) - 1:
                        count = 1
                        for items in advisor_list:
                            print(f"{count}. {items['first']} {items['last']}")
                            count += 1
                        print("Enter a number from the list to invite"
                              " an advisor.")
                        advisor = input("Enter number: ")
                        while int(advisor) not in range(count + 1):
                            print("Advisor is not in the list.")
                            advisor = input("Enter number: ")
                        inv_list.append(advisor_list[int(advisor) - 1]["ID"])
                        advisor_list.pop(int(advisor) - 1)
                        inv += 1
                    for projects in self.database.search("Projects.csv").table:
                        if projects["ID"] == str(proj_id):
                            print(f"Title: {projects['Title']}\n"
                                  f"Details: {projects['Details']}")
                            break
                    comment = input('Enter comment: ')
                    rating = input("Enter rating(1-10): ")
                    while float(rating) not in range(11):
                        print("Invalid rating.")
                        rating = input("Enter rating(1-10): ")
                    evaluation["evaluators"] = [int(i) for i in inv_list]
                    evaluation["comments"] = [comment]
                    evaluation["score"] = [int(rating)]
                    print(evaluation)
                    return
                else:
                    print("Showing projects that need evaluation.")
                    count = 1
                    proj_list = []
                    for items in self.database.search("evaluation.csv").table:
                        ids = items["evaluators"].strip('][').split(',')
                        ids = [int(i) for i in ids]
                        ids = [str(i) for i in ids]
                        if self.id in ids:
                            print(f"{count}. Title: {items['title']}"
                                  f" ID: {items['ID']}")
                            proj_list.append(items['ID'])
                            count += 1
                    if count == 1:
                        print("No projects found.")
                        return
                    project = input("Enter a project ID: ")
                    while project not in proj_list:
                        print("Invalid ID.")
                        project = input("Enter a project ID: ")
                    for projects in self.database.search("Projects.csv").table:
                        if projects["ID"] == str(project):
                            print(f"Evaluating {projects['Title']}\n"
                                  f"Details: {projects['Details']}")
                            break
                    comment = input('Enter comment: ')
                    rating = input("Enter rating(1-10): ")
                    while float(rating) not in range(11):
                        print("Invalid rating.")
                        rating = input("Enter rating(1-10): ")
                    for items in self.database.search("evaluation.csv").table:
                        if items["ID"] == str(project):
                            comments = items["comments"].strip('][').split(',')
                            comments = [i.strip(" ").strip("'")
                                        for i in comments]
                            comments.append(comment)
                            items["comments"] = comments
                            score = items["score"].strip('][').split(',')
                            score = [i.strip(" ").strip("'") for i in score]
                            score.append(rating)
                            items["score"] = score
                            if len(score) == int(items['no_advisors']):
                                items["date"] = time.asctime(time.localtime())
                                total_score = (sum([int(i) for i in score])
                                               / len(score))
                                for i in self.database.search(
                                        "Projects.csv").table:
                                    if i['ID'] == project:
                                        if total_score >= 7.5:
                                            i['Status'] = \
                                                "Awaiting finalization"
                                        else:
                                            i['Status'] = \
                                                "Awaiting re-evaluation"
                            print(items)
                            return
            elif action == "5":
                for projects in self.database.search("Projects.csv").table:
                    if projects["Advisor"] == str(self.id):
                        data = ["Awaiting finalization", "Awaiting "
                                                         "re-finalization"]
                        if projects["Status"] in data:
                            print(f"Confirming project: {projects['Title']}")
                            choice = input("confirm? (yes/no/cancel): ")
                            while choice not in ["yes", "no", "cancel"]:
                                print("Invalid choice.")
                                choice = input("confirm? (yes/no): ")
                            if choice == "cancel":
                                return
                            elif choice == "yes":
                                projects["Status"] = "Finished"
                                print(projects)
                                return
                            else:
                                projects["Status"] = "Awaiting re-finalization"
                                print(projects)
                                return
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
                    uid = str(len(
                        self.database.search("Projects.csv").table) + 1)
                    while len(uid) < 4:
                        uid = "0" + uid
                    project.update({"ID": uid})
                title = input("Enter project title: ")
                project.update({"Title": title})
                project.update(({"Lead": f"{self.id}"}))
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
                    if (students["ID"] not in
                            self.database.search("Projects.csv").table):
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
                            if students["type"] == "student":
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
                            request.update({"ID": projects["ID"]})
                            request.update({"Member": stu_id})
                            request.update({"Response": "Awaiting response"})
                            request.update(
                                {"Date of response": time.asctime(
                                    time.localtime())})
                            member_flag = True
                            break
                    if not member_flag:
                        print("You do not have a project. Create one first.")
                        return
                    else:
                        for requests in self.database.search(
                                "member_request.csv").table:
                            if request["ID"] in requests["ID"]:
                                if request["Member"] in requests["Member"]:
                                    print("Student already invited.")
                                    return
                        self.database.search(
                            "member_request.csv").insert([request])
                        print(self.database.search("member_request.csv"))
                elif choice == "2":
                    user_ids = []
                    print(self.database.search("member_request.csv").table)
                    count = 1
                    buffer = 0
                    print("Showing Accepted requests.")
                    for request in \
                            self.database.search("member_request.csv").table:
                        for project in \
                                self.database.search("Projects.csv").table:
                            if request["ID"] in project["ID"]:
                                if str(self.id) in project["Lead"]:
                                    if (request["Response"]
                                            == "Awaiting confirmation"):
                                        first = self.find_user(
                                            request['Member'])['first']
                                        last = self.find_user(
                                            request['Member'])['last']
                                        print(f"{count}. {first} {last} "
                                              f"ID: {request['Member']}")
                                        user_ids.append(request['Member'])
                                        request["Response"] = "pending"
                                        count += 1
                                        continue
                                    buffer += 1
                    if count == 1:
                        print("No pending request found.")
                        return
                    request = input("Enter a request number to "
                                    "approve or deny enter esc to exit: ")
                    if request == "esc":
                        for i in self.database.search(
                                "member_request.csv").table:
                            if i["Response"] == "pending":
                                i["Response"] = "Awaiting confirmation"
                        return
                    while int(request) not in range(count + 1):
                        print("Invalid request number.")
                        request = input("Enter a request number to "
                                        "approve or deny enter esc to exit: ")
                        if request == "esc":
                            for i in self.database.search(
                                    "member_request.csv").table:
                                if i["Response"] == "pending":
                                    i["Response"] = "Awaiting confirmation"
                            return
                    response = input("response (approve/deny): ")
                    if response == "deny":
                        self.database.search("member_request.csv").table[
                            int(request) - 1 + buffer].update(
                            {"Response": response})
                        for i in self.database.search(
                                "member_request.csv").table:
                            if i["Response"] == "pending":
                                i["Response"] = "Awaiting confirmation"
                            return
                    not_full = False
                    for project in self.database.search("Projects.csv").table:
                        if str(self.id) in project["Lead"]:
                            if project["Member1"] == "None":
                                project["Member1"] = (
                                    f"{user_ids[int(request) - 1]}")
                                not_full = True
                                break
                            elif project["Member2"] == "None":
                                project["Member2"] = (
                                    f"{user_ids[int(request) - 1]}")
                                not_full = True
                                break
                    if not not_full:
                        print("The project is full.")
                        return
                    for i in self.database.search("member_request.csv").table:
                        if i["Response"] == "pending":
                            i["Response"] = "Awaiting confirmation"
                    self.database.search("member_request.csv").table[
                        int(request) - 1 + buffer].update(
                        {"Response": "approved"})
                    self.database.search(
                        "persons.csv").update_table(
                        user_ids[int(request) - 1], "type", "member")
                    self.database.search(
                        "login.csv").update_table(
                        user_ids[int(request) - 1], "role", "member")
                    print(self.database.search("member_request.csv").table)
                    print()
                    print(self.database.search("Projects.csv").table)
            elif action == "4":
                self.read_project()
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
                    if advisors["type"] in ["faculty", "advisor"]:
                        advisor_list.append(advisors)
                        print(f"{count}. {advisors['first']} "
                              f"{advisors['last']}")
                        count += 1
                print("Enter a number from the list to invite an advisor\n "
                      "enter esc to exit.")
                advisor = input("Enter number: ")
                if advisor == "esc":
                    return
                while int(advisor) not in range(count):
                    print("Advisor is not in the list.")
                    advisor = input("Enter number: ")
                    if advisor == "esc":
                        return
                request = {}
                for projects in self.database.search("Projects.csv").table:
                    if str(self.id) in projects["Lead"]:
                        for requests in self.database.search(
                                "Advisor_request.csv").table:
                            if projects["ID"] in requests["ID"]:
                                print("You have already invited an advisor.")
                                return
                        first = advisor_list[int(advisor) - 1]['first']
                        last = advisor_list[int(advisor) - 1]['last']
                        request.update({"ID": projects["ID"]})
                        request.update({"Advisor": f"{first} {last}"})
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
                for projects in self.database.search("Projects.csv").table:
                    if str(self.id) in projects["Lead"]:
                        if projects["Status"] == "Awaiting finalization":
                            print("Submitting final project for finalization.")
                            choice = input("Confirm?(yes/no): ")
                            while choice != "yes" and choice != "no":
                                print("Invalid choice.")
                                choice = input("Confirm?(yes/no): ")
                            if choice == "yes":
                                print("Finalization request submitted.")
                                projects["Status"] = "finalizing"
                            else:
                                print("Aborting.")
                                return
                print("Submitting final project for evaluation.")
                choice = input("Confirm?(yes/no): ")
                while choice != "yes" and choice != "no":
                    print("Invalid choice.")
                    choice = input("Confirm?(yes/no): ")
                if choice == "yes":
                    print("Project submitted.")
                    for projects in self.database.search("Projects.csv").table:
                        if str(self.id) in projects["Lead"]:
                            if projects["Status"] != "Evaluating":
                                projects["Status"] = "Evaluating"
                                evaluate = {}
                                evaluate.update({"ID": projects["ID"]})
                                evaluate.update({"title": projects["Title"]})
                                evaluate.update({"no_advisors": 3})
                                evaluate.update({"comments": []})
                                evaluate.update({
                                    "evaluators": project["Advisor"]})
                                evaluate.update({"score": []})
                                evaluate.update({"date": "processing"})
                                self.database.search(
                                    "evaluation.csv").table.append(evaluate)
                elif choice == "no":
                    print("Aborting.")
                    return
        elif self.clearance == 4:
            if action == "1":
                check = False
                print("Your project invitations.")
                for inv in self.database.search("member_request.csv").table:
                    if str(self.id) == inv["Member"]:
                        for projects in (
                                self.database.search("Projects.csv").table):
                            if projects["ID"] == inv['ID']:
                                print(f"Project ID: {inv['ID']} "
                                      f"Title: {projects['Title']}")
                                check = True
                if not check:
                    print("No invitations.")
            elif action == "2":
                proj_list = []
                print("Eligible projects to join.")
                if len(self.database.search("member_request.csv").table) == 0:
                    print("No eligible projects to join.")
                    return
                for inv in self.database.search("member_request.csv").table:
                    if str(self.id) == inv["Member"]:
                        if inv["Response"] == "Awaiting response":
                            print(f"Project ID: {inv['ID']}")
                            proj_list.append(inv["ID"])
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
                        if projects == inv["ID"]:
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
                    for user in self.database.search("login.csv").table:
                        if user["ID"] == str(self.id):
                            self.clearance = 3
                            user["role"] = "lead"
        elif self.clearance == 5:
            self.read_project()
            print("Updating details. Enter esc to exit.")
            for project in self.database.search("Projects.csv").table:
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
    print(CsvReader("persons.csv").read())
    print()
    print(Table("persons", CsvReader("persons.csv").read()))
    print()
    print(Table("persons", CsvReader("persons.csv").read())
          .insert([{'friend': 'joe'}, {'animal': "duck"}]))
    print()
    # print(Table("persons", CSV_Reader("persons.csv").read())
    #       .update(0, "ID", 1))
    db = Database()
    x = Table("persons.csv", CsvReader("persons.csv").read())
    db.insert(x)
    y = Table("Advisor_request.csv",
              CsvReader("Advisor_request.csv").read())
    db.insert(y)
    z = Table("Projects.csv",
              CsvReader("Projects.csv").read())
    db.insert(z)
    a = Table("member_request.csv",
              CsvReader("member_request.csv").read())
    db.insert(a)
    b = Table("login.csv", CsvReader("login.csv").read())
    db.insert(b)
    x = b.update_table(9898118, "ID", "Number")
    print(x)
    clearance = int(input("Enter your clearance: "))
    u1 = User(clearance, '2472659', db)
    u1.manage()

    # table for clearance
    # 1 = admin
    # 2 = faculty
    # 3 = Lead
    # 4 student
    # 5 member
