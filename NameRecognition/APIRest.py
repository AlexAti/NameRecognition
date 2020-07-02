from flask import Flask
from flask_restful import Resource, Api, reqparse
from dill import load, dump
import pandas as pd
import sys
import os
import socket


sys.path[0] = sys.path[0].replace('NameRecognition/NameRecognition','NameRecognition')
sys.path[0] = sys.path[0].replace('NameRecognition\\NameRecognition','NameRecognition')
from NameRecognition.MLScreener import MLScreener

app = Flask('NameRecognitionAPIRest')
api = Api(app)

df_screen = pd.read_csv('data/names.csv')
print('df: ', df_screen.shape)

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
        from sqlalchmy import create_engine
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
        #host = socket.gethostbyname(socket.gethostname()),
        host = '192.168.0.28',
        debug = True if os.environ.get('NAME_RECOGNITION_DEBUG') == None else os.environ.get('NAME_RECOGNITION_DEBUG') == 'True',
        port = 5001 if os.environ.get('NAME_RECOGNITION_PORT') == None else int(os.environ.get('NAME_RECOGNITION_PORT'))
    )