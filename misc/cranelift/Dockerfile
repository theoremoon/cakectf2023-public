FROM python:3.9-slim@sha256:08a6a1666ddebe94becbec1986235cb8c321d2f7a7fd00f614befba5c1f23e67 AS base
WORKDIR /app
COPY distfiles/run.py run
COPY distfiles/toy    toy
COPY challenge/flag.txt /flag.txt
RUN  mv /flag.txt /flag-$(md5sum /flag.txt | awk '{print $1}').txt

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=60 JAIL_CPU=500 JAIL_MEM=20M JAIL_TMP_SIZE=8192
