# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
import json
import requests
import os
#
# from question.api.serializers import QuestionSerializer


AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'
REFRESH_ENDPOINT = AUTH_ENDPOINT + 'refresh/'


headers = {
    "Content-Type": "application/json",
}

data = {
	'username': 'by_shell_second8',
	'password': 'Lol1231',

}

data2 = {
	'username': 'JulitaTest',
	'password': 'Lol1231',

}

#
# r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
r2 = requests.post(AUTH_ENDPOINT, data=json.dumps(data2), headers=headers)
# token_random = r.json()['token']
token_skr = r2.json()['token']
# token = answer['token']
print(r2.json())


headers = {
    "Content-Type": "application/json",
	"Authorization": 'JWT ' + token_skr,
}


#
r = requests.get('http://127.0.0.1:8000/api/answer/summary/', headers=headers)
answer = r.json()
print(answer)




# headers2 = {
#     "Content-Type": "application/json",
# 	#"Authorization": 'JWT ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IlNrcmVjemtvIiwiZXhwIjoxNTQ4NTM2OTU3LCJlbWFpbCI6ImRhd2lkLnNrcmVjemtvQGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNTQ4NTM2NjU3fQ.B7TEAbIDNe7JJEbi70SN9m7FaIxtJpy_fRsN2C67sR0',
# }
# ENDPOINT = 'http://127.0.0.1:8000/api/answer/correct/'
#
# r = requests.get(ENDPOINT, headers=headers2)
# token = r.json()
# print(json.dumps(data))
# print(token)





# refresh_data = {
#     'token': token
# }
#
# new_response = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_data), headers=headers)
# new_token = new_response.json()['token']
#
# print(new_token)



# ENDPOINT = 'http://127.0.0.1:8000/api/answer/correct/'
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "JWT " + token,
# }
# data = json.dumps({
# 	'question': 'from shell?',
# 	'rank': 3
# })
#
#
# r = requests.get(ENDPOINT,  headers=headers)
# print(r.text)





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
