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

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/ctf/libc.so.6 /home/ctf/ld-linux-x86-64.so.2 /home/ctf/run.sh /home/ctf/flag.txt /home/ctf/chall /home/ctf /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_2b90aad1c876c786e7cc06558b1fee71477c93d88219cdaf1bfd12 -e RSCTF_DYNAMIC_FLAG_d91ba9ec2a7cda0b129f2f9e99186880b83ad05a0fab9c89 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
USER ctf
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
