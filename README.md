REST API web application that solves the problem of preparing and evaluating exam sheets.
-

**To create an example database, please run script EXAMPLE_DATABASE.py - remember to change admin credentials**

Web application contains:

For Staff user:
1) CRUD for Question with rank
2) CRUD multiple Answers for each Question with marking one as true 
3) Showing all Users and their grades (i.e. 7/10) - possibility to user filtering and ordering by grades and usernames with urls related to answers detail for each question
4) Showing which User answer was incorrect


For Users (students):
1) CRUD for Answers related to Questions - single choice 
2) Checking obtain grade
3) Checking list of Questions with added answer

-added permissions, JWT Authorization, ordering and filtering

-added unit tests