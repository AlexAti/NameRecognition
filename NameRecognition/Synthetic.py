import random
import pandas as pd

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