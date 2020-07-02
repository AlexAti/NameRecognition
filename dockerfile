FROM python:latest as nr_node
RUN apt-get install git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN python3.8 -m pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
ENV PYTHONPATH=/NameRecognition/
EXPOSE 5000
CMD [ "sleep", "3600"]
#CMD [ "pythno3", "-m", "uwsgi", "NameRecognition/wsgi.py"]

FROM nginx:latest as nr_balancer
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 5000

FROM python:latest as nr_test
RUN apt-get install git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
ENV PYTHONPATH=/NameRecognition/
CMD [ "python", "tests/test.py"]