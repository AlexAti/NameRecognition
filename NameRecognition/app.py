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
    import sys
    sys.path[0] = sys.path[0].replace('NameRecognition\\NameRecognition','NameRecognition')
    from NameRecognition import environ

from NameRecognition.Estimator import (
    TMEstimator,
    BatchEstimator
)
from NameRecognition.api import (
    OnDemand,
    Batch
)

app = Flask(__name__)
api = Api(app)

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

print('sql: ', df_screen.head(5))

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