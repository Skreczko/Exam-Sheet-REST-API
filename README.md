REST API web application that solves the problem of preparing and evaluating exam sheets.
-

**To create an example database, please run script EXAMPLE_DATABASE.py - remember to change admin credentials**

Application uses JWT tokens to authorization.

Web application contains:

For Staff user:
1) CRUD for Question with rank
2) CRUD multiple Answers for each Question with marking one as true 
3) Showing all Users and their grades (i.e. 7/10) - possibility to user filtering and ordering by grades and usernames with urls related to answers detail for each question
4) Showing which User answer was incorrect
5) Staff user cannot get grade or edit, update or delete users answers


For Users (students):
1) CRUD for Answers related to Questions - single choice 
2) Checking obtain grade
3) Checking list of Questions with added answer

-added permissions, JWT Authorization, ordering and filtering

-added unit tests


URLS
-
https://exam-sheet.herokuapp.com/api/auth/
1) Login site

https://exam-sheet.herokuapp.com/api/auth/register/
1) Register user

https://exam-sheet.herokuapp.com/api/auth/jwt/
1) Obtaining login token

https://exam-sheet.herokuapp.com/api/grades/ 

1) staff - list of users with their grades. URL to Question list with related user answer (+ description if correct)
2) user - getting grade with URL to Question list with related answer

https://exam-sheet.herokuapp.com/api/question/
1) staff - question list +  creating 

https://exam-sheet.herokuapp.com/api/question/1/
1) staff - updating, deleting question

https://exam-sheet.herokuapp.com/api/answer/admin/

1) staff - list of answers with related questions + creating 

https://exam-sheet.herokuapp.com/api/answer/admin/1/

1) staff - updating, deleting answer

https://exam-sheet.herokuapp.com/api/answer/summary/

1) user - list of question with owner answer + creating answer

https://exam-sheet.herokuapp.com/api/answer/summary/1/

1) user - answer detail - updating + deleting



