FROM python:3.11-slim-bullseye
COPY . /opt/holehe
WORKDIR /opt/holehe
RUN pip install --no-cache-dir .
