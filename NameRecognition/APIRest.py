from flask import Flask
from flask_restful import Resource, Api, reqparse
from dill import load, dump
import pandas as pd
import sys
import os

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
f = open('./NameRecognition/model/model.joblib', mode = 'wb+')
dump(streener, f)
f.close()

class APIScreening(Resource):
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

class APILoadDataset(Resource):
    def get(self):
        pass

class APILoadModel(Resource):
    def get(self):
        pass

class APIThreshold(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('threshold')
        args = parser.parse_args()
        streener.threshold = args['threshold']

api.add_resource(APIScreening, '/screening/')
api.add_resource(APILoadDataset, '/loaddataset/')
api.add_resource(APILoadModel, '/loadmodel/')
api.add_resource(APIThreshold, '/threshold/')

if __name__ == '__main__':
    #os.environ['NAME_RECOGNITION_PORT'] = '8082'
    print(os.environ)
    app.run(
        debug = True,
        port = 5000 if os.environ.get('NAME_RECOGNITION_PORT') == None else int(os.environ.get('NAME_RECOGNITION_PORT'))
    )