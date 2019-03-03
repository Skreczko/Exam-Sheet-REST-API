import json
import requests


"""	LOGIN AS ADMIN	"""

AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'
REFRESH_ENDPOINT = AUTH_ENDPOINT + 'refresh/'


headers = {
    "Content-Type": "application/json",
}

data = {
	'username': 'Admin1',		#change your username
	'password': 'Admin1',		#change your password

}

r_admin = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token_admin = r_admin.json()['token']

"""	CREATING QUESTIONS	"""

headers = {
    "Content-Type": "application/json",
	"Authorization": 'JWT ' + token_admin,
}

data_question1 = {
	"question": "Who was Albert Einstein?",
    "rank": 3
}

data_question2 = {
	"question": "In which year Maria Curie Sklodowska was born?",
    "rank": 2
}

data_question3 = {
	"question": "Who discovered light bulb?",
    "rank": 3
}

data_question4 = {
	"question": "Who discovered America?",
    "rank": 1
}


r_create_question1 = requests.post('http://127.0.0.1:8000/api/question/', data=json.dumps(data_question1), headers=headers)
r_create_question2 = requests.post('http://127.0.0.1:8000/api/question/', data=json.dumps(data_question2), headers=headers)
r_create_question3 = requests.post('http://127.0.0.1:8000/api/question/', data=json.dumps(data_question3), headers=headers)
r_create_question4 = requests.post('http://127.0.0.1:8000/api/question/', data=json.dumps(data_question4), headers=headers)
answer1 = r_create_question1.json()
answer2 = r_create_question2.json()
answer3 = r_create_question3.json()
answer4 = r_create_question4.json()
print(answer1)
print(answer2)
print(answer3)
print(answer4)

"""	CREATING ANSWERS """

r_admin = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token_admin = r_admin.json()['token']


headers = {
    "Content-Type": "application/json",
	  "Authorization": 'JWT ' + token_admin,
}

data_answer1_1 = {
    "question": 1,
    "answer_question": "Teacher",
    "is_correct": False
}

data_answer1_2 = {
    "question": 1,
    "answer_question": "Physicist",
    "is_correct": True
}

data_answer1_3 = {
    "question": 1,
    "answer_question": "Builder",
    "is_correct": False
}

data_answer2_1 = {
    "question": 2,
    "answer_question": "1745",
    "is_correct": False
}

data_answer2_2 = {
    "question": 2,
    "answer_question": "1895",
    "is_correct": False
}

data_answer2_3 = {
    "question": 2,
    "answer_question": "1867",
    "is_correct": True
}

data_answer2_4 = {
    "question": 2,
    "answer_question": "1876",
    "is_correct": False
}

data_answer3_1 = {
    "question": 3,
    "answer_question": "Thomas Edison",
    "is_correct": False
}

data_answer3_2 = {
    "question": 3,
    "answer_question": "Joseph Wilson Swan",
    "is_correct": True
}

data_answer3_3 = {
    "question": 3,
    "answer_question": "Alexander Graham Bell",
    "is_correct": False
}

data_answer3_4 = {
    "question": 3,
    "answer_question": "Lincoln Churchill",
    "is_correct": False
}

data_answer3_5 = {
    "question": 3,
    "answer_question": "Nicola Tesla",
    "is_correct": False
}

data_answer4_1 = {
    "question": 4,
    "answer_question": "Nicolaus Copernicus",
    "is_correct": False
}

data_answer4_2 = {
    "question": 4,
    "answer_question": "Columbus",
    "is_correct": True
}

r_create_answer1_1 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer1_1), headers=headers)
r_create_answer1_2 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer1_2), headers=headers)
r_create_answer1_3 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer1_3), headers=headers)
answer1_1 = r_create_answer1_1.json()
answer1_2 = r_create_answer1_2.json()
answer1_3 = r_create_answer1_3.json()
r_create_answer2_1 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer2_1), headers=headers)
r_create_answer2_2 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer2_2), headers=headers)
r_create_answer2_3 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer2_3), headers=headers)
r_create_answer2_4 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer2_4), headers=headers)
answer2_1 = r_create_answer2_1.json()
answer2_2 = r_create_answer2_2.json()
answer2_3 = r_create_answer2_3.json()
answer2_4 = r_create_answer2_4.json()
r_create_answer3_1 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer3_1), headers=headers)
r_create_answer3_2 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer3_2), headers=headers)
r_create_answer3_3 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer3_3), headers=headers)
r_create_answer3_4 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer3_4), headers=headers)
r_create_answer3_5 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer3_5), headers=headers)
answer3_1 = r_create_answer3_1.json()
answer3_2 = r_create_answer3_2.json()
answer3_3 = r_create_answer3_3.json()
answer3_4 = r_create_answer3_4.json()
answer3_5 = r_create_answer3_5.json()
r_create_answer4_1 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer4_1), headers=headers)
r_create_answer4_2 = requests.post('http://127.0.0.1:8000/api/answer/admin/', data=json.dumps(data_answer4_2), headers=headers)
answer4_1 = r_create_answer4_1.json()
answer4_2 = r_create_answer4_2.json()
print(answer1_1)
print(answer1_2)
print(answer1_3)
print(answer2_1)
print(answer2_2)
print(answer2_3)
print(answer2_4)
print(answer3_1)
print(answer3_2)
print(answer3_3)
print(answer3_4)
print(answer3_5)
print(answer4_1)
print(answer4_2)

"""	CREATING USERS	"""

headers = {
    "Content-Type": "application/json",

}

data_create_user1 = {
	"username": 			"TestUser1",
	"email":				"TestUser1@gmail.com",
    "password": 			"Lol123",
    "confirm_password": 	"Lol123",
}

data_create_user2 = {
	"username": 			"TestUser2",
	"email":				"TestUser2@gmail.com",
    "password": 			"Lol123",
    "confirm_password": 	"Lol123",
}

data_create_user3 = {
	"username": 			"TestUser3",
	"email":				"TestUser3@gmail.com",
    "password": 			"Lol123",
    "confirm_password": 	"Lol123",
}

r_create_user1 = requests.post('http://127.0.0.1:8000/api/auth/register/', data=json.dumps(data_create_user1), headers=headers)
r_create_user2 = requests.post('http://127.0.0.1:8000/api/auth/register/', data=json.dumps(data_create_user2), headers=headers)
r_create_user3 = requests.post('http://127.0.0.1:8000/api/auth/register/', data=json.dumps(data_create_user3), headers=headers)
answer1 = r_create_user1.json()
answer2 = r_create_user2.json()
answer3 = r_create_user3.json()
print(answer1)
print(answer2)
print(answer3)

"""	LOGIN AS TestUser1, TestUser2, TestUser3	"""

AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'
REFRESH_ENDPOINT = AUTH_ENDPOINT + 'refresh/'


headers = {
    "Content-Type": "application/json",
}

data_user1 = {
	'username': 'TestUser1',
	'password': 'Lol123',

}

data_user2 = {
	'username': 'TestUser2',
	'password': 'Lol123',

}

data_user3 = {
	'username': 'TestUser3',
	'password': 'Lol123',

}

r_user1 = requests.post(AUTH_ENDPOINT, data=json.dumps(data_user1), headers=headers)
r_user2 = requests.post(AUTH_ENDPOINT, data=json.dumps(data_user2), headers=headers)
r_user3 = requests.post(AUTH_ENDPOINT, data=json.dumps(data_user3), headers=headers)
token_user1 = r_user1.json()['token']
token_user2 = r_user2.json()['token']
token_user3 = r_user3.json()['token']

"""	CREATING ANSWERS - AS TestUser1 - all correct """

headers = {
    "Content-Type": "application/json",
    "Authorization": 'JWT ' + token_user1,
}

data_user1_answer1 = {
    "question": 1,
    "user_answer_id": 2,
}

data_user1_answer2 = {
    "question": 2,
    "user_answer_id": 6,
}

data_user1_answer3 = {
    "question": 3,
    "user_answer_id": 9,
}

data_user1_answer4 = {
    "question": 4,
    "user_answer_id": 14,
}

r_user1_answer1 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user1_answer1), headers=headers)
r_user1_answer2 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user1_answer2), headers=headers)
r_user1_answer3 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user1_answer3), headers=headers)
r_user1_answer4 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user1_answer4), headers=headers)
answer_user1_answer1 = r_user1_answer1.json()
answer_user1_answer2 = r_user1_answer2.json()
answer_user1_answer3 = r_user1_answer3.json()
answer_user1_answer4 = r_user1_answer4.json()
print(answer_user1_answer1)
print(answer_user1_answer2)
print(answer_user1_answer3)
print(answer_user1_answer4)

"""	CREATING ANSWERS - AS TestUser2 - first and last correct """

headers = {
    "Content-Type": "application/json",
    "Authorization": 'JWT ' + token_user2,
}

data_user2_answer1 = {
    "question": 1,
    "user_answer_id": 2,
}

data_user2_answer2 = {
    "question": 2,
    "user_answer_id": 5,
}

data_user2_answer3 = {
    "question": 3,
    "user_answer_id": 8,
}

data_user2_answer4 = {
    "question": 4,
    "user_answer_id": 14,
}

r_user2_answer1 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user2_answer1), headers=headers)
r_user2_answer2 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user2_answer2), headers=headers)
r_user2_answer3 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user2_answer3), headers=headers)
r_user2_answer4 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user2_answer4), headers=headers)
answer_user2_answer1 = r_user2_answer1.json()
answer_user2_answer2 = r_user2_answer2.json()
answer_user2_answer3 = r_user2_answer3.json()
answer_user2_answer4 = r_user2_answer4.json()
print(answer_user2_answer1)
print(answer_user2_answer2)
print(answer_user2_answer3)
print(answer_user2_answer4)


"""	CREATING ANSWERS - AS TestUser3 - only first correct """

headers = {
    "Content-Type": "application/json",
    "Authorization": 'JWT ' + token_user3,
}

data_user3_answer1 = {
    "question": 1,
    "user_answer_id": 2,
}

data_user3_answer2 = {
    "question": 2,
    "user_answer_id": 7,
}

data_user3_answer3 = {
    "question": 3,
    "user_answer_id": 10,
}

data_user3_answer4 = {
    "question": 4,
    "user_answer_id": 13,
}

r_user3_answer1 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user3_answer1), headers=headers)
r_user3_answer2 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user3_answer2), headers=headers)
r_user3_answer3 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user3_answer3), headers=headers)
r_user3_answer4 = requests.post('http://127.0.0.1:8000/api/answer/summary/', data=json.dumps(data_user3_answer4), headers=headers)
answer_user3_answer1 = r_user3_answer1.json()
answer_user3_answer2 = r_user3_answer2.json()
answer_user3_answer3 = r_user3_answer3.json()
answer_user3_answer4 = r_user3_answer4.json()
print(answer_user3_answer1)
print(answer_user3_answer2)
print(answer_user3_answer3)
print(answer_user3_answer4)


""" CHECK PERMISSIONS FOR .../API/GRADES/"""
headers = {
    "Content-Type": "application/json",
    "Authorization": 'JWT ' + token_user1,
}

r_user3_answer1 = requests.get('http://127.0.0.1:8000/api/grades/', headers=headers)
answer = r_user3_answer1.json()
print(answer)
