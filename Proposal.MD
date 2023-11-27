# Project evaluation step
### Introduction
This doc will outline the necessary steps for evaluating
senior projects. The evaluation step will be added after the project has been
submitted and before it is approved by the advisor.
The evaluation step will involve a group of faculty personnel
who will help evaluate the project and provide feedback.

### The evaluation steps
1. The lead student submit his project for evaluation.
The system then assigns a number of faculty and advisors to review the project.
The default number is 5 people and the system will attempt to assign personnel based on their
current commitments.


2. The system then notifies the selected faculty personnel. The notification
will include the project details as well as final date of acceptance.


3. Faculty personnel will be able to accept or decline to be an evaluator
and have access to the project  in question and all it's details.


4. The evaluators will then evaluate the project based on a fixed criteria and
provide feedback as well as grade the project on a scale of 1 to 10.


5. The students and the advisor will be able to view the evaluation in order
to plan their next course of action.


6. The students will have the option to make changes to their project then 
finalize the project if they score 7.5 or more in the evaluation. The students 
may revise the project again if they do not meet the criteria after 
implementing changes to the project then send the project for re-evaluation.


7. If the project is finalized the advisor may approve or deny the final 
project based on the criteria. If a project is denied the students will
be notified and will have to submit the project to the advisor for 
re-evaluation

### Relevant code
The following is a rough draft of the code relevant to the evaluation step
which maybe subject to change.
1. sending evaluation proposal
```commandline
user.send_eval(project_id)
```
2. Accessing the project for evaluators
```commandline
if project["status"] == "requesting evaluation"
    print(project_details)
```
3. Grading the project
```commandline
eval_rq = database.search(eval.csv).table
for project in eval_rq:
    if project_id == project["ID"]
        comment = input("some comment: ")
        grade = input("some grade (1:10): ")
    eval_rq["comments"].append(comment)
    eval_rq["Grade"].append(grade)
```
4. Reading project
```commandline
if user.self_id in eval.csv:
    print("Evaluation available")
    user.read_eval()
```
5. read comments
```commandline
for eval in eval.csv:
    if self.id in eval["members"]
    print(eval["comments"])
```
6. Finalize project
```commandline
from user.manage when clearance == 3 and action == "6":
    if project["status"] == "Awaiting finalization" or "Awaiting re-finalization"
        eval_rq["step"] = "Finalizing"
        
```
7. Approve project
```commandline
for eval in eval.csv:
    if eval["step"] = "Finalizing"
    print("Approve project?")
    if yes:
        project["Status"] = "Finished"
    else:
        eval["step"] = "Awaiting re-finalization"
```

once again this code is just a proof of concept and will not work if ran