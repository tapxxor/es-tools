FROM python:3.5.6-alpine

RUN pip3 install elasticsearch
RUN pip3 install faker

ADD app.py /app.py

ENTRYPOINT exec python3 app.py