FROM python:3.11-slim-bullseye
COPY . /opt/mailscope
WORKDIR /opt/mailscope
RUN python3 setup.py install
