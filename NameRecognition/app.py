from flask import Flask
from flask_restful import Resource, Api, reqparse
from dill import load, dump
from sqlalchemy import create_engine
import pandas as pd
import sys
import os

os.chdir(path = '/NameRecognition')
#from NameRecognition import environ

from NameRecognition.MLScreener import MLScreener
from NameRecognition.api import (
    OnDemand,
    Screening
)

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

screener = MLScreener(
    threshold = threshold,
    score_factor = score_factor,
    df_screen = df_screen,
    key_screen = 'key_screen',
    value_screen = 'value_screen',
    key_party = 'key_party',
    value_party = 'value_party',
    verbose = False
)

screener.fit(df_screen['value_screen'])
f = open('./model/model.joblib', mode = 'wb+')
dump(screener, f)
f.close()

api.add_resource(
    OnDemand, 
    '/ondemand/',
    resource_class_kwargs = {
        'screener': screener
    }
)
api.add_resource(
    Screening, 
    '/screening/',
    resource_class_kwargs = {
        'screener': screener
    }
)

if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        debug = True if os.environ.get('NAME_RECOGNITION_DEBUG') == None else os.environ.get('NAME_RECOGNITION_DEBUG') == 'true',
        port = int(os.environ.get('NAME_RECOGNITION_PORT'))
    )