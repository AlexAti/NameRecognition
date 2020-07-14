from flask import Flask
from flask_restful import Resource, Api, reqparse
from dill import load, dump
from sqlalchemy import create_engine
import pandas as pd
import sys
import os
import platform

if platform.system() != 'Windows': 
    os.chdir(path = '/NameRecognition')
else:
    from NameRecognition import environ

from NameRecognition.Estimator import TMEstimator
from NameRecognition.api import (
    OnDemand,
    Batch
)

app = Flask(__name__)
api = Api(app)

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

print('sql: ', df_screen.shape)

estimator = TMEstimator(
    threshold = threshold,
    score_factor = score_factor,
    df_screen = df_screen,
    key_screen = 'key_screen',
    value_screen = 'value_screen',
    key_party = 'key_party',
    value_party = 'value_party'
)

estimator.fit(df_screen['value_screen'])
f = open('./model/model.joblib', mode = 'wb+')
dump(estimator, f)
f.close()

api.add_resource(
    OnDemand, 
    '/ondemand/',
    resource_class_kwargs = {
        'estimator': estimator
    }
)
api.add_resource(
    Batch, 
    '/batch/',
    resource_class_kwargs = {
        'estimator': estimator
    }
)

if __name__ == '__main__':
    params = {
        'host': "0.0.0.0",
        'debug': True,
        'port': 5000
    }
    if os.environ.get('NAME_RECOGNITION_DEBUG') != None:
        params['debug'] = os.environ['NAME_RECOGNITION_DEBUG']
    if os.environ.get('NAME_RECOGNITION_PORT') != None:
        params['port'] = int(os.environ['NAME_RECOGNITION_PORT'])
    app.run(**params)