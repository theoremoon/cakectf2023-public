FROM debian:11-slim AS base
WORKDIR /app
COPY distfiles/chall run
COPY challenge/flag.txt /flag.txt

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=300 JAIL_CPU=500 JAIL_MEM=10M
