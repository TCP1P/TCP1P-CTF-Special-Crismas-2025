FROM ghcr.io/foundry-rs/foundry:latest

USER root
RUN apt-get update && \
    apt-get install -y python3 socat && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1001 -s /bin/bash ctf

RUN mkdir -p /home/ctf/chall/src

COPY ./Setup.sol /home/ctf/chall/src
COPY ./GiftDistributor.sol /home/ctf/chall/src
COPY ./chall.py /home/ctf/chall/src/chall.py
COPY ./run.sh /home/ctf/chall/src/run.sh
COPY ./flag.txt /home/ctf/chall/src/flag.txt

WORKDIR /home/ctf/chall/src
RUN forge init --force && forge build

RUN chown -R ctf:ctf /home/ctf/chall
RUN chmod -R 755 /home/ctf/chall

USER ctf
WORKDIR /home/ctf/chall/src

EXPOSE 8011 8545

CMD ["./run.sh"]
