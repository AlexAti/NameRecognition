from flask import Flask
from flask_restful import Resource, Api, reqparse
from dill import load, dump
from sqlalchemy import create_engine
import pandas as pd
import sys
import os

sys.path[0] = sys.path[0].replace('NameRecognition/NameRecognition','NameRecognition')
sys.path[0] = sys.path[0].replace('NameRecognition\\NameRecognition','NameRecognition')
from NameRecognition.MLScreener import MLScreener

app = Flask(__name__)
api = Api(app)

df_screen = pd.read_csv('data/names.csv')

con = create_engine(
    '{dialect}://{user}:{password}@{url}:{port}'.format(
        dialect = os.environ.get('NAME_RECOGNITION_SQL_DIALECT'),
        user = os.environ.get('NAME_RECOGNITION_SQL_USER'),
        password = os.environ.get('NAME_RECOGNITION_SQL_PASSWORD'),
        url = os.environ.get('NAME_RECOGNITION_SQL_URL'),
        port = os.environ.get('NAME_RECOGNITION_SQL_PORT')
    )
).connect()

df_screen = pd.read_sql_query(
    sql = os.environ.get('NAME_RECOGNITION_QUERY_SCREEN'),
    con = con,
    index_col = None
)

print(df_screen.head(5))

"""score_factor = pd.read_sql_query(
    sql = os.environ.get('NAME_RECOGNITION_QUERY_SCORE_FACTOR'),
    con = con,
    index_col = None
)

threshold = pd.read_sql_query(
    sql = os.environ.get('NAME_RECOGNITION_QUERY_THRESHOLD'),
    con = con,
    index_col = None
)"""

print('sql: ', df_screen.shape)

streener = MLScreener(
    threshold = 0.50,
    df_screen = df_screen,
    key_screen = 'key_screen',
    value_screen = 'value_screen',
    key_party = 'key_party',
    value_party = 'value_party',
    verbose = False
)

streener.fit(df_screen['value_screen'])
f = open('./model/model.joblib', mode = 'wb+')
dump(streener, f)
f.close()

class APIOnDemand(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('key_party')
        parser.add_argument('value_party')
        args = parser.parse_args()
        print(args['key_party'])
        print(args['value_party'])
        df = pd.DataFrame([{
            'key_party': args['key_party'],
            'value_party': args['value_party'],
        }])
        df_filter = streener.screening(df)
        return {
            'df_filter': df_filter.to_dict(orient = 'list'),
            'screen': streener.screen.to_dict(orient = 'list')
        }

class APIScreening(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url')
        parser.add_argument('query')
        args = parser.parse_args()
        print(args['url'])
        print(args['query'])
        from sqlalchemy import create_engine
        con = create_engine(args['url'])
        df = pd.read_sql_query(
            con,
            sql = args['query'],
            index_col = None
        )
        df_filter = streener.screening(df)
        return {
            'df_filter': df_filter.to_dict(orient = 'list'),
            'screen': streener.screen.to_dict(orient = 'list')
        }

class APILoadDataset(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url')
        parser.add_argument('query')
        args = parser.parse_args()

class APILoadModel(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('path')
        args = parser.parse_args()

class APIThreshold(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('threshold')
        args = parser.parse_args()
        streener.threshold = args['threshold']

api.add_resource(APIOnDemand, '/ondemand/')
api.add_resource(APIScreening, '/screening/')

api.add_resource(APILoadDataset, '/loaddataset/')
api.add_resource(APILoadModel, '/loadmodel/')
api.add_resource(APIThreshold, '/threshold/')

if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        debug = True if os.environ.get('NAME_RECOGNITION_DEBUG') == None else os.environ.get('NAME_RECOGNITION_DEBUG') == 'true',
        port = 5000 if os.environ.get('NAME_RECOGNITION_PORT') == None else int(os.environ.get('NAME_RECOGNITION_PORT'))
    )