FROM python:latest as nr_node
RUN apt-get update && apt-get install -y \
    git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN python3 -m pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
EXPOSE 5000
CMD [ "python3", "NameRecognition/Synthetic.py"]

FROM postgres:latest as nr_db
ADD postgresql.conf /usr/share/postgresql/
COPY sql/ /docker-entrypoint-initdb.d/
