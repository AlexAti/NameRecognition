import unittest

import sys
sys.path[0] = sys.path[0].replace('\\tests','')

import pandas as pd

class NameRecognitionTest(unittest.TestCase):
    def test_ondemand(self):
        import requests
        import json

        session = requests.Session()

        h = session.get(
            url = 'http://localhost:5000/ondemand/',
            params = {
                'key_party': "prueba1",
                'value_party': "minger felita girijarani",
            }
        ).json()
        print(h)

    def test_ondemand1(self):
        import requests
        import json

        session = requests.Session()

        h = session.get(
            url = 'http://localhost:5000/ondemand/',
            params = {
                'key_party': "prueba1",
                'value_party': "minger felita girijarani",
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
    
    def test_synthetic(self):
        print(sys.path)

    def test_synthetic_csv(self):
        from NameRecognition.Synthetic import synthetic_csv
        synthetic_csv()

    def test_db_connexion(self):
        from sqlalchemy import create_engine
        con = create_engine('postgresql://postgres:password@localhost:5432').connect()

    def test_environ(self):
        import os
        print(os.environ['VSCODE_PID'])

if __name__ == "__main__":
    unittest.main(verbosity = 2)