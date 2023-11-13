FROM sagemath/sagemath:10.1

ENV DEBIAN_FRONTEND noninteractive

USER root
RUN apt-get update && apt-get install -yqq socat

USER sage
ADD challenge/server.sage server.sage

CMD socat TCP-L:9999,fork,reuseaddr EXEC:"sage server.sage"
