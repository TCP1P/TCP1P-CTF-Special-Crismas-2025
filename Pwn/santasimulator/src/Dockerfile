FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y xinetd && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m ctf

WORKDIR /app
COPY --chmod=555 chall .
COPY flag.txt /
RUN cd / && mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt && \
    chown root:root /flag-*.txt && chmod 444 /flag-*.txt && \
    chown -R root:root /app && chmod -R 555 /app

RUN echo "chall stream tcp nowait ctf /app/chall chall" >> /etc/inetd.conf && \
    echo "chall 5000/tcp" >> /etc/services

EXPOSE 5000
CMD ["xinetd", "-dontfork", "-inetd_compat"]
