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