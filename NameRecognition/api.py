from flask_restful import Resource, reqparse
import pandas as pd
import string
import random

from NameRecognition.ExtraFields import ExtraFields

class OnDemand(Resource):
    def __init__(self, estimator):
        self.estimator = estimator
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('key_party')
        self.parser.add_argument('value_party')
        self.parser.add_argument('birth_date')
        self.parser.add_argument('birth_country')
        self.parser.add_argument('identifier')
        self.parser.add_argument('gender')

    def get(self):
        args = self.parser.parse_args()
        print(args['key_party'])
        print(args['value_party'])
        df = pd.DataFrame([{
            'key_party': args['key_party'],
            'value_party': args['value_party'],
            'birth_date': args['birth_date'],
            'birth_country': args['birth_country'],
            'identifier': args['identifier'],
            'gender': args['gender']
        }])
        adjacency_matrix = self.estimator.predict(df)
        adjacency_matrix = ExtraFields(
            df_screen = self.estimator.df_screen,
            adjacency_matrix = adjacency_matrix,
            df_party = df,
            score_factor = self.estimator.score_factor,
            threshold = self.estimator.threshold,
            key_party = self.estimator.key_party,
            key_screen = self.estimator.key_screen
        )
        return(adjacency_matrix.to_json())

class Batch(Resource):
    def __init__(self, estimator):
        self.estimator = estimator
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('url')
        self.parser.add_argument('query')
    
    def get(self):
        args = self.parser.parse_args()
        print(args['url'])
        print(args['query'])
        from sqlalchemy import create_engine
        conn = create_engine(args['url']).connect()
        df = pd.read_sql_query(
            con = conn,
            sql = args['query'],
            index_col = None
        )
        adjacency_matrix = self.estimator.predict(df)
        adjacency_matrix = ExtraFields(
            df_screen = self.estimator.df_screen,
            adjacency_matrix = adjacency_matrix,
            df_party = df,
            score_factor = self.estimator.score_factor,
            threshold = self.estimator.threshold,
            key_party = self.estimator.key_party,
            key_screen = self.estimator.key_screen
        )
        adjacency_matrix_name = 'df_filter_' + ''.join(
            random.choices(string.ascii_lowercase, k = 32)
        )
        adjacency_matrix.to_sql(
            name = adjacency_matrix_name,
            schema = 'wlf',
            con = conn,
            index = False
        )
        return {
            'adjacency_matrix': adjacency_matrix_name
        }