import requests
import json

url = 'https://api.github.com/users'
user = 'VladislavShatov'


response = requests.get(f'{url}/{user}/repos')
if response.ok:
    pass

j_data = response.json()

for el in j_data:
    print(el['name'])

with open ('repos_names.json', 'w') as f:
    json.dump(j_data, f)



