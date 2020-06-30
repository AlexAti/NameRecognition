import time
import requests
import json
import random
import threading

print('Esperando')
time.sleep(120)
print('Tiempo finalizado')


mtest = 1000
ninstances = 5
threads = []
url = 'http://namerecognition_name_recognition_{}:5000/screening/'

class TestApiRest(threading.Thread):
    def run(self):
        for _ in range(int(mtest/ninstances)):
            session = requests.Session()
            respond = session.get(
                url = url.format(random.randint(1,ninstances)),
                params = {
                    'key_party': "prueba1",
                    'value_party': "kashdon shirleeta tequana",
                }
            ).json()
            print(respond)

for i in range(ninstances):
    thread = TestApiRest()
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()

