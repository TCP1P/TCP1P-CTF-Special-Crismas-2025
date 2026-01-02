FROM python:3.10-slim

RUN apt-get -y update && apt-get -y install socat --fix-missing && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/chall

COPY jail.py jail.py
COPY flag.txt /flag.txt
RUN chmod 644 /flag.txt && mv /flag.txt /flag-$(head -c8 /dev/urandom | md5sum | tr -cd '[:alnum:]')

EXPOSE 5000
ENTRYPOINT socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"python3 ./jail.py",su=nobody
