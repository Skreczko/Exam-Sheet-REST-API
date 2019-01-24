# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
import json
import requests
import os
#
# from question.api.serializers import QuestionSerializer


AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/jwt/'
REFRESH_ENDPOINT = AUTH_ENDPOINT + 'refresh/'


headers = {
    "Content-Type": "application/json",
}

data = {
	'username': 'TestUser1',
	'password': 'Lol123456789',
}



r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token = r.json()['token']
print(token)

refresh_data = {
    'token': token
}

new_response = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_data), headers=headers)
new_token = new_response.json()['token']

print(new_token)



ENDPOINT = 'http://127.0.0.1:8000/api/answer/correct/'

headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT " + token,
}
data = json.dumps({
	'question': 'from shell?',
	'rank': 3
})


r = requests.get(ENDPOINT,  headers=headers)
print(r.text)





# r2 = requests.get(REFRESH_ENDPOINT, data=json.dumps(data2), headers=headers)
# token2 = r2.json()['token']
# print(token2)
# print(token==token2)



#
# from answer.api.serializers import UserAnswerSerializer
#
# data = {
# 	'question': 2,
# 	'user_answer_id': 4
#
# }
#
# serializer = UserAnswerSerializer(data=data)
# serializer.is_valid()
