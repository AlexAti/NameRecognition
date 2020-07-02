from flask import Flask
from flask_restful import Resource, Api, reqparse
from dill import load, dump
import pandas as pd
import sys
import os
import socket
import requests
import json
import random

app = Flask('NameRecognitionAPIRest')
api = Api(app)

ninstances = 1
url = 'http://namerecognition_name_recognition_{}:5001/'
url = '192.168.0.28:5001/'

class APIOnDemand(Resource):
    def get(self):
        print('hola')
        parser = reqparse.RequestParser()
        parser.add_argument('key_party')
        parser.add_argument('value_party')
        args = parser.parse_args()
        session = requests.Session()
        respond = session.get(
            url = (url + 'screening/').format(
                random.randint(1,ninstances)
            ),
            params = {
                'key_party': args['key_party'],
                'value_party': args['value_party'],
            }
        ).json()
        print('respuesta: ', respond)
        return(respond)

class APIScreening(Resource):
    def get(self):
        pass

class APIInstance(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ninstances')
        args = parser.parse_args()
        ninstances = int(args['ninstances'])
        return ({'ninstances': args['ninstances']})

api.add_resource(APIOnDemand, '/ondemand/')
api.add_resource(APIScreening, '/screening/')

api.add_resource(APIInstance, '/ninstances/')

if __name__ == '__main__':
    app.run(
        #host = socket.gethostbyname(socket.gethostname()),
        host = '192.168.0.28',
        debug = True if os.environ.get('NAME_RECOGNITION_DEBUG') == None else os.environ.get('NAME_RECOGNITION_DEBUG') == 'True',
        port = 5000 if os.environ.get('NAME_RECOGNITION_PORT') == None else int(os.environ.get('NAME_RECOGNITION_PORT'))
    )