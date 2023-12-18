# Final project for 2023's 219114/115 Programming I

# List of included files:

- Advisor_request.csv
- database.py
- evaluation.csv
- login.csv
- member_request.csv
- persons.csv
- project_manage.py
- Projects.csv
- Proposal.MD
- README.md
- TODO.md

# How to run the project:

Run the project using project_manage.py

for more details consult Proposal and TODO. The basic process goes as follows.
1. Log in with a student account then become a lead
2. Create a project invite an advisor/members update the project (members are optional)
3. Log in to the invited account(s) and accept/decline the invitations
   (if the advisor declines repeat steps 1-3)
4. Log in to the lead account and submit the project for evaluation
5. Log in to the advisor account invite other evaluators and evaluate the project
6. Log in to the other evaluator accounts and evaluate the project
   (note that there is no evaluator type if you forgot who you invited the ids
are in evaluation.csv)
7. Once all evaluators have evaluated the project, Log in to the lead account
and choose Manage project to read the evaluation.
8. Submit the project for finalization or re-evaluation
9. Log in to the advisor account to confirm/deny project finalization (if the
project was sent for re-evaluation repeat steps 4-9)
10. (Optional) Log in with any member of the project to read project details.

# List of class and their functions

### class CsvReader

This class reads .csv files

- read: reads the csv file and converts it to a list of dictionaries.

### class Database

This class stores various tables

- insert: inserts a piece of data into the database
- search: searches for a table with the inputted table name

### class Table

This class is a list of dictionaries with an assigned name

- insert: inserts items in a list into the Table (in hindsight this should have
been named join)
- update_table: updates a key value pair in a dict when the provided ID matches
an id in the Table
- update_dict: updates an entire dictionary in the Table if the provided ID 
exists

### class User

This class is used to run the program

- manage: runs the program by running other functions in this class
- lead_deny_all: This function automatically declines all invitations once 
a student becomes a lead
- check_advisor: checks if the user is an advisor
- finish_project: checks if the user has a project and if it is finished
- read_eval: reads evaluations
- read_project: reads user's project details
- find_user: finds the user with the provided id in a Table and returns their dictionary
- find_username: returns the username of the inputted id
- help: prints the users commands
- actions: A collective mess of code which executes code to do various actions
depending on the action provided (Unfortunately due to my lack of planning
this function is very poorly designed and barely legible and as such the table
you are about to see is just this function)

# Table of actions

| Role            | Action                   | Methods | class | completion |
|-----------------|--------------------------|---------|-------|------------|
| Admin           | Update item              | Manage  | user  | 100%       |
| Admin           | Update dictionary        | Manage  | user  | 100%       |
| Faculty/Advisor | View request             | Manage  | user  | 90%        |
| Faculty/Advisor | Respond to request       | Manage  | user  | 100%       |
| Faculty/Advisor | See project details      | Manage  | user  | 100%       |
| Faculty/Advisor | Evaluate projects        | Manage  | user  | 100%       |
| Advisor         | Approve project          | Manage  | user  | 100%       |
| Lead            | Create project           | Manage  | user  | 100%       |
| Lead            | Find members             | Manage  | user  | 100%       |
| Lead            | Invite/Add students      | Manage  | user  | 100%       |
| Lead/Member     | Manage project           | Manage  | user  | 100%       |
| Lead            | Submit project           | Manage  | user  | 100%       |
| student         | View project invitations | Manage  | user  | 90%        |
| student         | Respond to invitations   | Manage  | user  | 100%       |
| student         | Become a Lead            | Manage  | user  | 100%       |

### Known bugs and missing features

- If a prompt asks for a number but a string is inputted the
program explodes.
- There is no notification system for advisors/faculty/students for
invitations.