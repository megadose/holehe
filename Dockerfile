FROM python:3.11-slim-bullseye
COPY . /opt/holehe
WORKDIR /opt/holehe

RUN pip install requests

RUN pip install httpx
RUN python3 setup.py install
