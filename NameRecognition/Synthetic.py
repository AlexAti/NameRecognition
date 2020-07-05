import random
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.types import *
from datetime import datetime

def synthetic_csv(m = 3000):
    f = open('data/names.txt', mode = 'r', encoding = 'utf8')
    lista = list(map(lambda s: s.replace('\n', ''),f.readlines()))
    dictionary = []
    for i in range(m):
        dictionary.append({
            'value_screen': ' '.join(random.choices(lista, k=3)).replace("'",''),
            'key_screen': 'key_' + str(i)
        })
    pd.DataFrame(dictionary).to_csv('data/names.csv', index = False)

def synthetic_db(m = 3000):
    f = open('data/names.txt', mode = 'r', encoding = 'utf8')
    lista = list(map(lambda s: s.replace('\n', ''),f.readlines()))
    dictionary = []
    for i in range(m):
        dictionary.append({
            'value_screen': ' '.join(random.choices(lista, k=3)).replace("'",''),
            'key_screen': 'key_' + str(i),
            'birth_date': str(random.randint(1900,2020)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(10,27)),
            'birth_country': random.choice(['ES','FR','AG','AF','ID','IR']),
            'identifier': str(random.randint(1000000,9000000)) + random.choice(['b','c','d','f','g','h','j'])
        })
    
    df = pd.DataFrame(dictionary)
    print(df.head(5))
    con = create_engine(
        '{dialect}://{user}:{password}@{url}:{port}'.format(
            dialect = os.environ.get('NAME_RECOGNITION_SQL_DIALECT'),
            user = os.environ.get('NAME_RECOGNITION_SQL_USER'),
            password = os.environ.get('NAME_RECOGNITION_SQL_PASSWORD'),
            url = os.environ.get('NAME_RECOGNITION_SQL_URL'),
            port = os.environ.get('NAME_RECOGNITION_SQL_PORT')
        ), isolation_level = "AUTOCOMMIT"
    ).connect()
    for row in df.iterrows():
        sql = "insert into wlf.screening (value_screen,key_screen,birth_date) values ('"
        sql += row['value_screen'] + "','"
        sql += row['key_screen'] + "','"
        sql += row['birth_date'] + "','"
        sql += row['birth_country'] + "','"
        sql += row['identifier'] + "');"
        con.execute(sql)

if __name__ == "__main__":
    synthetic_db(m = 100000)