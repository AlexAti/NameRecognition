FROM python:3.8.3-alpine3.12 as NameRecognition

RUN apk add git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN pip install -r /NameRecognition/requirements.txt
CMD [ "sh" ]