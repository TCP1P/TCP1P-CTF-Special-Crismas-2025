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

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/ctf/chall/src/flag.txt /home/ctf/chall/src/run.sh /home/ctf/chall/src/chall.py /home/ctf/chall/src /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_fc1cb2fe57c -e RSCTF_DYNAMIC_FLAG_b4711 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
USER ctf
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
