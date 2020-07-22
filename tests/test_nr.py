import unittest
import sys
sys.path[0] = sys.path[0].replace('\\tests','')

class NameRecognitionTest(unittest.TestCase):
    def test_api_ondemand(self):
        import requests
        import json
        import pandas as pd

        session = requests.Session()
        result = session.get(
            url = 'http://localhost:5000/ondemand/',
            params = {
                'key_party': "prueba1",
                'value_party': "msial tona kuplerski",
                'birth_date': "1902-01-20",
                'birth_country': "AG",
                'identifier': "3724412b",
                "gender": "female"
            }
        ).json()
        adjacency_matrix = pd.read_json(result)
        print(adjacency_matrix.shape)
        if adjacency_matrix.shape[0] != 0:
            print(adjacency_matrix.loc[0])
        else:
            print('Empty result')

    def test_api_batch(self):
        import requests
        import json
        import pandas as pd
        import os
        import platform
        from NameRecognition import environ

        session = requests.Session()
        url = os.environ.get('NAME_RECOGNITION_SQL_URL')
        url = url.replace(
            'localhost',
            'namerecognition_postgres_1'
        )
        print(url)

        h = session.get(
            url = 'http://localhost:5000/batch/',
            params = {
                'url': url,
                'query': "select * from wlf.party order by key_party desc limit 2000 ;",
            }
        ).json()
        print(h)

    def test_batch(self):
        import pandas as pd
        import os
        from sqlalchemy import create_engine
        from NameRecognition.Estimator import (
            TMEstimator,
            BatchEstimator
        )
        from NameRecognition.api import (
            OnDemand,
            Batch
        )
        from NameRecognition import environ
        con = create_engine(
            os.environ.get('NAME_RECOGNITION_SQL_URL')
        ).connect()

        df_screen = pd.read_sql_query(
            sql = os.environ.get('NAME_RECOGNITION_QUERY_SCREEN'),
            con = con,
            index_col = None
        )

        score_factor = pd.read_sql_query(
            sql = "SELECT * FROM WLF.SCORE_FACTOR WHERE factor_key = '" + os.environ['NAME_RECOGNITION_SCORE_FACTOR'] + "'",
            con = con,
            index_col = None
        ).loc[0]
        print(score_factor)

        threshold = pd.read_sql_query(
            sql = "SELECT * FROM WLF.THRESHOLD WHERE threshold_key = '" + os.environ['NAME_RECOGNITION_THRESHOLD'] + "'",
            con = con,
            index_col = None
        ).loc[0]
        print(threshold)

        estimator = BatchEstimator(
            estimator = TMEstimator(
                threshold = threshold,
                score_factor = score_factor,
                df_screen = None,
                key_screen = 'key_screen',
                value_screen = 'value_screen',
                key_party = 'key_party',
                value_party = 'value_party'
            ),
            df_screen = df_screen,
            screen_batch_size = int(os.environ['NAME_RECOGNITION_SCREEN_BATCH_SIZE'])
        )

        estimator.fit(df_screen['value_screen'])

        df = pd.read_sql_query(
            con = con,
            sql = "select * from wlf.party order by key_party desc limit 1000 ;",
            index_col = None
        )
        adjacency_matrix = estimator.predict(df)

if __name__ == "__main__":
    unittest.main(verbosity = 2)