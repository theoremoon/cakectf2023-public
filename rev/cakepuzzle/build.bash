#!/bin/bash
set -eux

docker run --rm -u $(id -u):$(id -g) -v ./challenge/:/mnt/challenge/ python:3-bullseye bash -c "cd /mnt/challenge/; python3 gen.py"
