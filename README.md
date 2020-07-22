# NameRecognition

NameRecognition es un módulo escrito en Python pensado para detectar patrones de similitud complejos entre cádenas de texto de longitud corta. Comunmente la aplicación de este tipo de algoritmos viene dado por un nivel de abstracción superior. Se realizan cotejos a nivel de listas, y se obtiene como resultado la lista de emparejamientos entre ambas. Una de ellas suele adquirir un role estático, definiendose en este proyecto como lista de cotejo.

## Instalación
La instalación de este módulo se realiza mediante la siguiente instrucción:
```bash
python setup.py install
```

## Algoritmo
La extracción de patrones se realiza en 3 pasos:
1) [Limpieza de stopwords](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html): se entrena un modelo parametrizable basado en frecuencias que extrae las palabras menos significativas para un conjunto de cadenas de texto. Posteriormente dichas cadenas se sustituyen por vacío.
2) [Frecuencia de términos](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html): sobre el conjunto de cadenas limpio se calcula un modelo basado en frecuencias de caracteres. Como resultado de su aplicación se obtiene del corpus una matriz dispersa de vectores de la misma dimensión.
3) [Similitud coseno](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html#sklearn.metrics.pairwise.cosine_similarity): para cada posible par de coordenadas extraidas de los dos conjuntos se aplica la similitud coseno dando como resultado la matriz de adyacencia que conecta dichos conjuntos.
4) Comparación de campos segundarios.

## Servicio y despliegue
Presenta un despliegue en forma de servicio API RESTFUL implementado sobre la biblioteca [flask](https://flask.palletsprojects.com/en/1.1.x/) que implementa principalmente dos funcionalidades:

**Cotejo individual**

Una entidad se coteja contra la lista de cotejo estático cargada en la instancia en forma 1 VS ALL, obteniendo como resultado el conjunto de emperajamientos para esta entidad concreta.

```python
import requests
import json

session = requests.Session()

h = session.get(
    url = 'http://localhost:5000/ondemand/',
    params = {
        'key_party': "test",
        'value_party': "minger felita girijarani",
        'birth_date': "1999-03-26",
        'birth_country': "ID",
        'identifier': "8346836g"
    }
).json()
```

La salida es estructura en dos componentes dentro de la respuesta:
* Entidad contejada con puntuación máxima sobre el conjunto de emparejamientos.
* Tabla de emparejamientos con puntuaciones individuales.

**Cotejo colectivo**

Se realiza una extracción de una base de datos relacional de una lista dinámica que se coteja en forma ALL VS ALL contra la lista estática de cotejo cargada en la instancia.

```python
import requests
import json

session = requests.Session()

h = session.get(
    url = 'http://localhost:5000/ondemand/',
    params = {
        'url': "postgresql+pg8000://scott:tiger@localhost/test",
        'sql': "select * from table_example",
    }
).json()
```
La salida indica la conexión y las tablas de base de datos donde se ha volcado el cotejo.

## Docker
El proyecto se puede construir y arrancar facilmente usando la imagen Docker descrita en el fichero DockerFile:
```dockerfile
FROM python:latest as nr_node
RUN apt-get update && apt-get install -y \
    git \
    uwsgi \
    uwsgi-src && \
    apt-get clean
ADD github /
RUN git clone https://`cat /github`@github.com/rojo1997/NameRecognition && \
    rm github && \
    python3 -m pip install -r /NameRecognition/requirements.txt && \
    export PYTHON=python3.8 && \
    uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python38" && \
    mv python38_plugin.so /usr/lib/uwsgi/plugins/python38_plugin.so && \
    chmod 644 /usr/lib/uwsgi/plugins/python38_plugin.so
WORKDIR /NameRecognition/NameRecognition/
EXPOSE 5000
CMD [ "uwsgi", "--ini", "server.ini"]
```

## Docker-Compose

Ejemplo parametrizado del contenedo:
```yml
version: "3.8"
services:
  nr_node:
    image: namerecognition
    networks:
      nr_networks:
    restart: always
    depends_on:
      - postgres
    environment: 
      - NAME_RECOGNITION_SQL_DIALECT=postgresql
      - NAME_RECOGNITION_SQL_USER=postgres
      - NAME_RECOGNITION_SQL_PASSWORD=password
      - NAME_RECOGNITION_SQL_URL=namerecognition_postgres_1
      - NAME_RECOGNITION_SQL_PORT=5432
      - NAME_RECOGNITION_PORT=5000
      - NAME_RECOGNITION_DEBUG=true
      - NAME_RECOGNITION_QUERY_SCREEN=SELECT * FROM WLF.screening;
      - NAME_RECOGNITION_SCORE_FACTOR=key_0
      - NAME_RECOGNITION_THRESHOLD=key_0
    ports:
      - "5000:5000"
  postgres:
    image: datamodel
    volumes: 
      - data_postgres:/var/lib/postgresql/data
    restart: always
    environment: 
      - POSTGRES_PASSWORD=password
    networks:
      nr_networks:
    ports:
      - "5432:5432" # postgres

networks:
  nr_networks:
    driver: bridge
volumes: 
  data_postgres:
```

Escalabilidad del servicio
```bash
docker-compose -f "docker-compose.yml" up -d --scale nr_node=5
```

## Dependencias
NameRecognition requiere de:
* flask
* flask_restful
* pandas
* dill
* sklearn
* requests

El servidor RESTful se levanta sobre un servidor de aplicaciones [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) que configura el número de procesos para concurrencia del servicio y le da la posibilidad de ser balanceado.

## Testing Module

El fichero [environ.py](https://github.com/rojo1997/NameRecognition/blob/master/NameRecognition/environ.py) aporta 
un entorno de variables de sistema equivalente al desplegado por la imagen Docker.

```python
import os
os.environ['NAME_RECOGNITION_SQL_URL'] = 'postgresql://postgres:password@localhost:5432'
os.environ['NAME_RECOGNITION_PORT'] = '5000'
os.environ['NAME_RECOGNITION_DEBUG'] = 'true'
os.environ['NAME_RECOGNITION_QUERY_SCREEN'] = 'SELECT * FROM WLF.screening LIMIT 100000;'
os.environ['NAME_RECOGNITION_SCORE_FACTOR'] = 'key_0'
os.environ['NAME_RECOGNITION_THRESHOLD'] = 'key_0'
os.environ['NAME_RECOGNITION_SCREEN_BATCH_SIZE'] = '10000'
os.environ['NAME_RECOGNITION_PARTY_BATCH_SIZE'] = '25000'
```
