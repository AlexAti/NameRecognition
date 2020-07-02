# NameRecognition

NameRecognition es un módulo de Python pensado para detectar patrones de similitud complejos entre cádenas de texto de longitud pequeña. Comunmente la aplicación de este tipo de algoritmos viene dado por un conjunto de cotejo y un conjunto sobre el que cotejar. 

## Algoritmo
La extracción de patrones se realiza en 3 pasos:
1) [Limpieza de stopwords](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html): se entrena un modelo parametrizable basado en frecuencias que extrae las palabras menos significativas para un conjunto de cadenas de texto. Posteriormente dichas cadenas se sustituyen por vacío.
2) [TF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html): sobre el conjunto de cadenas limpio se calcula un modelo basado en frecuencias de caracteres. Como resultado de su aplicación se obtiene del corpus una matriz dispersa de vectores de la misma dimensión.
3) [Similitud coseno](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html#sklearn.metrics.pairwise.cosine_similarity): para cada posible par de coordenadas extraidas de los dos conjuntos se aplica la similitud coseno dando como resultado la matriz de adyacencia que conecta dichos conjuntos.

## Servicio y despliegue
Presenta un despliegue en forma de servicio API RESTFUL implementado sobre la biblioteca [flask](https://flask.palletsprojects.com/en/1.1.x/) que implementa principalmente dos funcionalidades:

**Cotejo individual**

```python
import requests
import json

session = requests.Session()

h = session.get(
    url = 'http://localhost:5000/ondemand/',
    params = {
        'key_party': "test",
        'value_party': "minger felita girijarani",
    }
).json()
```

**Cotejo colectivo**
```python
import requests
import json

session = requests.Session()

h = session.get(
    url = 'http://localhost:5000/ondemand/',
    params = {
        'url': "postgresql+pg8000://scott:tiger@localhost/test",
        'sql': "select key_party, value_party from table_example",
    }
).json()
```

Incluye una imagen Docker que permite escalabilidad.

## Dependencias
NameRecognition requiere de:
* sklearn
* pandas
* dill
* flask
