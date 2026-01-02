FROM ubuntu:22.04

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1001 ctf

WORKDIR /home/ctf

COPY chall /home/ctf/chall
COPY flag.txt /home/ctf/flag.txt
COPY run.sh /home/ctf/run.sh

RUN chown root:root /home/ctf/chall /home/ctf/flag.txt /home/ctf/run.sh && \
    chmod 555 /home/ctf/chall && \
    chmod 444 /home/ctf/flag.txt && \
    chmod 555 /home/ctf/run.sh

USER ctf

EXPOSE 8011

CMD ["./run.sh"]
