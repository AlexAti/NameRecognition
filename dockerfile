FROM python:latest as nr_node
RUN apt-get update && apt-get install -y \
    git \
    uwsgi \
    uwsgi-src \
    uwsgi-plugin-python3
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN python3 -m pip install -r /NameRecognition/requirements.txt
ENV PYTHON=python3
WORKDIR /NameRecognition/
ENV PYTHONPATH=/NameRecognition/
EXPOSE 5000
CMD [ "python3", "NameRecognition/app.py"]

FROM postgres:latest as nr_db
ADD postgresql.conf /usr/share/postgresql/
