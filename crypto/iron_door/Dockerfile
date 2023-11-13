FROM python:3.10-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -yqq socat
RUN pip install pycryptodome
ADD challenge/server.py server.py

ENV FLAG "CakeCTF{}"
CMD socat TCP-L:9999,fork,reuseaddr EXEC:"python server.py"
