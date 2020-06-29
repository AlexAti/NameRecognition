import unittest

import sys
sys.path[0] = sys.path[0].replace('\\tests','')

import pandas as pd

class NameRecognitionTest(unittest.TestCase):
    def test_Threshold(self):
        import requests
        import json

        session = requests.Session()

        h = session.get(
            url = 'http://localhost:5000/screening/',
            params = {
                'key_party': "prueba1",
                'value_party': "kashdon shirleeta tequana",
            }
        ).json()
        print(h)

    
    def test_synthetic(self):
        print(sys.path)

    def test_synthetic_csv(self):
        from NameRecognition.Synthetic import synthetic_csv
        synthetic_csv()

if __name__ == "__main__":
    unittest.main(verbosity = 2)