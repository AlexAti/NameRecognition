import random
import pandas as pd
import numpy as np
import os
import platform
from sqlalchemy import create_engine
from sqlalchemy.types import *
from datetime import datetime

from NameRecognition import environ

con = create_engine(
    '{dialect}://{user}:{password}@{url}:{port}'.format(
        dialect = os.environ.get('NAME_RECOGNITION_SQL_DIALECT'),
        user = os.environ.get('NAME_RECOGNITION_SQL_USER'),
        password = os.environ.get('NAME_RECOGNITION_SQL_PASSWORD'),
        url = os.environ.get('NAME_RECOGNITION_SQL_URL'),
        port = os.environ.get('NAME_RECOGNITION_SQL_PORT')
    )
).connect()

f = open('data/names.txt', mode = 'r', encoding = 'utf8')
lista = list(map(lambda s: s.replace('\n', ''),f.readlines()))
screening = []
for i in range(100000):
    screening.append({
        'value_screen': ' '.join(random.choices(lista, k=3)).replace("'",''),
        'key_screen': 'key_' + str(i),
        'birth_date': str(random.randint(1900,2020)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(10,27)),
        'birth_country': random.choice(['ES','FR','AG','AF','ID','IR']),
        'identifier': str(random.randint(1000000,9000000)) + random.choice(['b','c','d','f','g','h','j'])
    })
screening = pd.DataFrame(screening)

party = []
for i in range(9000):
    party.append({
        'value_party': ' '.join(random.choices(lista, k=3)).replace("'",''),
        'key_party': 'key_' + str(i),
        'birth_date': str(random.randint(1900,2020)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(10,27)),
        'birth_country': random.choice(['ES','FR','AG','AF','ID','IR']),
        'identifier': str(random.randint(1000000,9000000)) + random.choice(['b','c','d','f','g','h','j'])
    })
party_hit = []
for i in range(9000,10000):
    row = {
        'value_party': random.choice(screening['value_screen'].to_list()),
        'key_party': 'key_' + str(i),
        'birth_date': str(random.randint(1900,2020)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(10,27)),
        'birth_country': random.choice(['ES','FR','AG','AF','ID','IR']),
        'identifier': str(random.randint(1000000,9000000)) + random.choice(['b','c','d','f','g','h','j'])
    }
    party_hit.append(row['key_party'])
    party.append(row)

party = pd.DataFrame(party)

score_factor = []
score_factor.append({
    'factor_key': 'key_0',
    'value_factor': 1.0,
    'birth_date_factor': 10.0,
    'birth_country_factor': 5.0,
    'identifier_factor': 50.0
})
score_factor.append({
    'factor_key': 'key_1',
    'value_factor': 1.0,
    'birth_date_factor': 15.0,
    'birth_country_factor': 10.0,
    'identifier_factor': 25.0
})
score_factor = pd.DataFrame(score_factor)

threshold = []
threshold.append({
    'threshold_key': 'key_0',
    'value_threshold': 70.0,
    'global_threshold': 100.0
})
threshold.append({
    'threshold_key': 'key_1',
    'value_threshold': 60.0,
    'global_threshold': 90.0
})
threshold = pd.DataFrame(threshold)


alert = []
for i in range(1000):
    alert.append({
        'alert_id': 'key_' + str(i),
        'key_party': random.choice(party_hit),
        'status_id': random.choices(
            population = [0,1],
            weights = [0.99,0.01],
            k = 1
        )[0]
    })
alert = pd.DataFrame(alert)

hit = []
for i in range(2000):
    hit.append({
        'hit_id': 'key_' + str(i),
        'alert_id': random.choice(alert['alert_id'].tolist()),
        'key_screen': 'syntetic_' + str(i),
        'score': random.random() * 100.0,
        'birth_country_hit': random.choice([True,False]),
        'birth_date_hit': random.choice([True,False]),
        'identifier_hit': random.choice([True,False])
    })
hit = pd.DataFrame(hit)

screening.to_sql(
    con = con,
    name = 'screening',
    schema = 'wlf',
    if_exists = 'append',
    index = False
)

party.to_sql(
    con = con,
    name = 'party',
    schema = 'wlf',
    if_exists = 'append',
    index = False
)

score_factor.to_sql(
    con = con,
    name = 'score_factor',
    schema = 'wlf',
    if_exists = 'append',
    index = False
)

threshold.to_sql(
    con = con,
    name = 'threshold',
    schema = 'wlf',
    if_exists = 'append',
    index = False
)

alert.to_sql(
    con = con,
    name = 'alert',
    schema = 'wlf',
    if_exists = 'append',
    index = False
)

hit.to_sql(
    con = con,
    name = 'hit',
    schema = 'wlf',
    if_exists = 'append',
    index = False
)