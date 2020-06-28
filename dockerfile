FROM python:latest as NameRecognition

RUN apt-get install git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN pip install -r /NameRecognition/requirements.txt
CMD [ "python", "/NameRecognition/NameRecognition/APIRest.py"]