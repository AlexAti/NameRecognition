FROM python:latest as NameRecognition

RUN apt-get install git
RUN git clone https://rojo1997:ogame522@github.com/rojo1997/NameRecognition
RUN pip install -r /NameRecognition/requirements.txt
WORKDIR /NameRecognition/
#CMD [ "bash"]
ENV PYTHONPATH=/NameRecognition/
CMD [ "python", "NameRecognition/APIRest.py"]