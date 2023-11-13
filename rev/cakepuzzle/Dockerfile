FROM debian:11-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -yqq xinetd libevent-dev
RUN groupadd -r chal && useradd -r -g chal chal

RUN echo '#!/bin/bash\n\
service xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service pwn\n\
{\n\
  type = UNLISTED\n\
  disable = no\n\
  socket_type = stream\n\
  protocol = tcp\n\
  wait = no\n\
  user = chal\n\
  bind = 0.0.0.0\n\
  port = 9999\n\
  server = /home/chal/chal\n\
}' > /etc/xinetd.d/pwn
RUN chmod 500 /etc/init.sh
RUN chmod 444 /etc/xinetd.d/pwn
RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD challenge/flag.txt /flag.txt
RUN chmod 444 /flag.txt

WORKDIR /home/chal
ADD challenge/chal .
RUN chmod 550 chal

RUN chown -R root:chal /home/chal
RUN service xinetd restart
