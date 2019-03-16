FROM python:3.6-slim-stretch as build

RUN pip install svgwrite 

WORKDIR /usr/data


