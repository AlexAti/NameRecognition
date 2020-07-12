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
                'value_party': "miquisha shinsuke blouncie",
                'birth_date': "1988-03-26",
                'birth_country': "AG",
                'identifier': "5100235j"
            }
        ).json()
        df_filter = pd.DataFrame(result['df_filter'])
        print(df_filter)
        screen = pd.DataFrame(result['screen'])
        print(screen)

    def test_batch(self):
        import requests
        import json
        import os
        from NameRecognition import environ

        session = requests.Session()
        url = '{dialect}://{user}:{password}@{url}:{port}'.format(
            dialect = os.environ.get('NAME_RECOGNITION_SQL_DIALECT'),
            user = os.environ.get('NAME_RECOGNITION_SQL_USER'),
            password = os.environ.get('NAME_RECOGNITION_SQL_PASSWORD'),
            url = os.environ.get('NAME_RECOGNITION_SQL_URL'),
            port = os.environ.get('NAME_RECOGNITION_SQL_PORT')
        )
        print(url)

        h = session.get(
            url = 'http://localhost:5000/batch/',
            params = {
                'url': url,
                #'query': "select key_screen as key_party,value_screen as value_party,birth_date,birth_country,identifier from wlf.screening limit 1000;",
                'query': "select key_party,value_party,birth_date,birth_country,identifier from wlf.party limit 10000;",
            }
        ).json()
        print(h)

    def test_ninstances(self):
        import requests
        import json

        session = requests.Session()

        h = session.get(
            url = 'http://localhost:5000/ninstances/',
            params = {
                'ninstances': '5'
            }
        ).json()
        print(h)

    def test_environ(self):
        import os
        print(os.environ['VSCODE_PID'])

if __name__ == "__main__":
    unittest.main(verbosity = 2)