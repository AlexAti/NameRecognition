import time
import requests
import json
import random

print('Esperando')
time.sleep(120)
print('Tiempo finalizado')
session = requests.Session()

m = 500
n = 5
cluster = []

for i in range(5):
    url = 'http://namerecognition_name_recognition_{}:5000/screening/'.format(random.randint(1,n))
    respond = session.get(
        url = url,
        params = {
            'key_party': "prueba1",
            'value_party': "kashdon shirleeta tequana",
        }
    ).json()
    print(respond)
