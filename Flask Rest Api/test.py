import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {'likes': 1, 'views': 5, 'name': 'video 1'},
    {'likes': 12, 'views': 5, 'name': 'video 2'},
    {'likes': 3, 'views': 5, 'name': 'video 3'}
]

for i in range(len(data)):
    response = requests.put(BASE + 'video/' + str(i), data[i])
    print(response.json())

# response = requests.get(BASE + 'helloworld/alexis/1')
# response = requests.delete(BASE + 'video/0')
# print(response)
input()
response = requests.get(BASE + 'video/2')
print(response.json())
