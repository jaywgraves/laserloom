FROM python:3.6-slim-stretch as build
WORKDIR /usr/data
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY laserloom.py .