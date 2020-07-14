import unittest

import sys
sys.path[0] = sys.path[0].replace('\\tests','')

import pandas as pd

class NameRecognitionTest(unittest.TestCase):
    def test_ondemand(self):
        import requests
        import json

        session = requests.Session()
        result = session.get(
            url = 'http://localhost:5000/ondemand/',
            params = {
                'key_party': "prueba1",
                'value_party': "udelka jesan fiffer",
                'birth_date': "1952-02-17",
                'birth_country': "FR",
                'identifier': "1170675h"
            }
        ).json()
        #adjacency_matrix = pd.DataFrame(result)
        adjacency_matrix = pd.read_json(result)
        print(adjacency_matrix.loc[0])

    def test_batch(self):
        import requests
        import json
        import os
        import platform
        from NameRecognition import environ

        session = requests.Session()
        url = '{dialect}://{user}:{password}@{url}:{port}'.format(
            dialect = os.environ.get('NAME_RECOGNITION_SQL_DIALECT'),
            user = os.environ.get('NAME_RECOGNITION_SQL_USER'),
            password = os.environ.get('NAME_RECOGNITION_SQL_PASSWORD'),
            url = 'namerecognition_postgres_1',#os.environ.get('NAME_RECOGNITION_SQL_URL'),
            port = os.environ.get('NAME_RECOGNITION_SQL_PORT')
        )
        print(url)

        h = session.get(
            url = 'http://localhost:5000/batch/',
            params = {
                'url': url,
                'query': "select * from wlf.party limit 8000;",
            }
        ).json()
        print(h)

if __name__ == "__main__":
    unittest.main(verbosity = 2)