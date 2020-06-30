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
url = 'http://namerecognition_name_recognition_{}:5000/screening/'

class APIScreening(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('key_party')
        parser.add_argument('value_party')
        args = parser.parse_args()
        session = requests.Session()
        respond = session.get(
            url = url.format(
                random.randint(1,ninstances)
            ),
            params = {
                'key_party': args['key_party'],
                'value_party': args['value_party'],
            }
        ).json()
        return(respond)

api.add_resource(APIScreening, '/screening/')

if __name__ == '__main__':
    app.run(
        host = socket.gethostbyname(socket.gethostname()),
        debug = True if os.environ.get('NAME_RECOGNITION_DEBUG') == None else os.environ.get('NAME_RECOGNITION_DEBUG') == 'True',
        port = 5000 if os.environ.get('NAME_RECOGNITION_PORT') == None else int(os.environ.get('NAME_RECOGNITION_PORT'))
    )