FROM python:latest as NameRecognition

RUN apt-get install git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
ENV PYTHONPATH=/NameRecognition/
ENV NAME_RECOGNITION_PORT=8080
CMD [ "python", "NameRecognition/APIRest.py"]