FROM ubuntu:22.04

RUN apt update && apt install -y socat patchelf && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1001 ctf

WORKDIR /home/ctf

COPY chall /home/ctf/chall
COPY flag.txt /home/ctf/flag.txt
COPY run.sh /home/ctf/run.sh
COPY ld-linux-x86-64.so.2 /home/ctf/ld-linux-x86-64.so.2
COPY libc.so.6 /home/ctf/libc.so.6

RUN patchelf --set-interpreter ./ld-linux-x86-64.so.2 /home/ctf/chall && \
    patchelf --set-rpath . /home/ctf/chall && \
    chown root:root /home/ctf/* && \
    chmod 555 /home/ctf/chall /home/ctf/run.sh /home/ctf/ld-linux-x86-64.so.2 && \
    chmod 444 /home/ctf/flag.txt /home/ctf/libc.so.6

USER ctf

EXPOSE 8011

CMD ["./run.sh"]
