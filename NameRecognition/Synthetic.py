import random
import pandas as pd
import os
from sqlalchemy import create_engine

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
            'key_screen': 'key_' + str(i)
        })
    con = create_engine(
        '{dialect}://{user}:{password}@{url}:{port}'.format(
            dialect = os.environ.get('NAME_RECOGNITION_SQL_DIALECT'),
            user = os.environ.get('NAME_RECOGNITION_SQL_USER'),
            password = os.environ.get('NAME_RECOGNITION_SQL_PASSWORD'),
            url = os.environ.get('NAME_RECOGNITION_SQL_URL'),
            port = os.environ.get('NAME_RECOGNITION_SQL_PORT')
        )
    ).connect()
    pd.DataFrame(dictionary).to_sql(
        name = 'screening',
        schema = 'WLF',
        con = con,
        if_exists = 'append'
    )

if __name__ == "__main__":
    synthetic_db()