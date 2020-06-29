FROM python:latest as name_recognition
RUN apt-get install git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
ENV PYTHONPATH=/NameRecognition/
EXPOSE 5000
CMD [ "python", "NameRecognition/APIRest.py"]


FROM python:latest as test
RUN apt-get install git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
ENV PYTHONPATH=/NameRecognition/
CMD [ "python", "tests/test.py"]