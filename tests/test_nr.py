import unittest
import sys
sys.path[0] = sys.path[0].replace('\\tests','')

class NameRecognitionTest(unittest.TestCase):
    def test_ondemand_docker(self):
        import requests
        import json
        import pandas as pd

        session = requests.Session()
        result = session.get(
            url = 'http://localhost:5000/ondemand/',
            params = {
                'key_party': "prueba1",
                'value_party': "musial tona kuplerski",
                'birth_date': "1902-01-20",
                'birth_country': "AG",
                'identifier': "3724412b",
                "gender": "female"
            }
        ).json()
        adjacency_matrix = pd.read_json(result)
        if adjacency_matrix.shape[0] != 0:
            print(adjacency_matrix.loc[0])
        else:
            print('Empty result')

    def test_batch(self):
        import requests
        import json
        import pandas as pd
        import os
        import platform
        from NameRecognition import environ

        session = requests.Session()
        url = os.environ.get('NAME_RECOGNITION_SQL_URL')
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