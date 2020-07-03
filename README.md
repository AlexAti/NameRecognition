# NameRecognition

NameRecognition es un módulo escrito en Python pensado para detectar patrones de similitud complejos entre cádenas de texto de longitud corta. Comunmente la aplicación de este tipo de algoritmos viene dado por un nivel de abstracción superior. Se realizan cotejos a nivel de listas, y se obtiene como resultado la lista de emparejamientos entre ambas. Una de ellas suele adquirir un role estático, definiendose en este proyecto como lista de cotejo.

## Instalación
Una posible instalación sería la siguiente:
```bash
python setup.py install
```

## Algoritmo
La extracción de patrones se realiza en 3 pasos:
1) [Limpieza de stopwords](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html): se entrena un modelo parametrizable basado en frecuencias que extrae las palabras menos significativas para un conjunto de cadenas de texto. Posteriormente dichas cadenas se sustituyen por vacío.
2) [TF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html): sobre el conjunto de cadenas limpio se calcula un modelo basado en frecuencias de caracteres. Como resultado de su aplicación se obtiene del corpus una matriz dispersa de vectores de la misma dimensión.
3) [Similitud coseno](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html#sklearn.metrics.pairwise.cosine_similarity): para cada posible par de coordenadas extraidas de los dos conjuntos se aplica la similitud coseno dando como resultado la matriz de adyacencia que conecta dichos conjuntos.

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
    }
).json()
```

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
        'sql': "select key_party, value_party from table_example",
    }
).json()
```

## Docker
El proyecto se puede construir y arrancar facilmente usando la imagen Docker descrita en el fichero DockerFile:
```docker
FROM python:latest as nr_node
RUN apt-get update && apt-get install -y \
    git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN python3 -m pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
EXPOSE 5000
CMD [ "python3", "NameRecognition/app.py"]
```
Puesto que el proyecto implementa una conexión estándar a base de datos relacional desde la que se puede cargar tanto la lista de cotejo como la lista contra lo que cotejar, nativamente permite una escalabilidad haciendo uso de docker-compose. Un ejemplo de orquestación simple sería el siguiente:
```docker
version: "3.8"
services:
  nr_node:
    build: 
      context: .
      target: nr_node
```

## Docker-Compose

Que se podría arrancar 5 instancias del contenedor de la siguiente forma:
```docker
version: "3.8"
services:
  nr_node:
    build: 
      context: .
      target: nr_node
    networks:
      nr_networks:
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
      - NAME_RECOGNITION_QUERY_SCREEN=SELECT key_screen, value_screen FROM screening;
```

## Dependencias
NameRecognition requiere de:
* flask
* flask_restful
* pandas
* dill
* sklearn
* requests

## Testing Module
