REST API web application that solves the problem of preparing and evaluating exam sheets.
-

**To create an example database, please run script EXAMPLE_DATABASE.py - remember to change admin credentials**

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
http://127.0.0.1:8000/api/auth/
1) Login site

http://127.0.0.1:8000/api/auth/register/
1) Register user

http://127.0.0.1:8000/api/auth/jwt/
1) Obtaining login token

http://127.0.0.1:8000/api/grades/ 

1) staff - list of users with their grades. URL to Question list with related user answer (+ description if correct)
2) user - getting grade with URL to Question list with related answer

http://127.0.0.1:8000/api/question/
1) staff - question list +  creating 

http://127.0.0.1:8000/api/question/<id>
1) staff - updating, deleting question

http://127.0.0.1:8000/api/answer/admin/

1) staff - list of answers with related questions + creating 

http://127.0.0.1:8000/api/answer/admin/<id>

1) staff - updating, deleting answer

http://127.0.0.1:8000/api/answer/summary/

1) user - list of question with owner answer + creating answer

http://127.0.0.1:8000/api/answer/summary/<id>/

1) user - answer detail - updating + deleting



