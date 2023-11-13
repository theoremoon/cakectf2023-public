FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk update
RUN adduser -D ctf
RUN pip install Flask

ARG FLAG
ENV FLAG=${FLAG}

WORKDIR /app
ADD distfiles .
RUN python3 init_db.py
RUN chown -R root:ctf .
RUN chmod 444 database.db
