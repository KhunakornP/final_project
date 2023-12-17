# To do:
- [x] add a better interface for admins
- [x] add more checks so user inputs don't brick some actions
- [x] more code optimizations
- [x] better menus
- [x] create an evaluation step
- [ ] PEP 8 (I tried)

# Usage
The program will first read all .csv files in the directiory and put in 
the database.
Then the user will be prompted to log in by
entering their username and password.

If the user entered a valid username and password the program will allow them
to preform actions based on their role.


(Unfortunately due to how project_manage was written the data will
only update once the user logs out. While the oversight can be fixed
it would necessitate me to restructure the entire code and I do not have
enough time to fix it sorry in advance.)

# Roles
There are currently 5 roles and each role can do the following

### Admins:

- Can edit the database using various functions.


### Faculty

- View and respond to advisor requests.
- Become an advisor to a project.
- See all projects and their details.
- Evaluate created projects.
### Advisors

- Same as a faculty.
- Can approve projects that are currently being supervised.
### Leads

- Create a project.
- View and modify their project as well as their
evaluations.
- Send an invitation to students to join their project.
- Send an invitation to a faculty or advisor to become their project advisor.


### students

- View and respond to their project invitations.
- Become a lead.

### members

- View and modify their project as well as their.
evaluations


