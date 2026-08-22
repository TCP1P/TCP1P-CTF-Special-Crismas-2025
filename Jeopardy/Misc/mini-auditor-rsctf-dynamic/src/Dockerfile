FROM python:3.10-slim

RUN apt-get -y update && apt-get -y install socat --fix-missing && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/chall

COPY jail.py jail.py
COPY flag.txt /flag.txt
RUN chmod 644 /flag.txt && mv /flag.txt /flag-$(head -c8 /dev/urandom | md5sum | tr -cd '[:alnum:]')

EXPOSE 5000
# Original final-stage ENTRYPOINT is wrapped by RSCTF at runtime.

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /opt/chall/jail.py /opt/chall /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_6570865942ee427eec026fc60eaf3b47d25cfdcc4 -e RSCTF_DYNAMIC_FLAG_cdc7d44f5e71a098089a959005f74ac2782 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint", "/bin/sh", "-c", "socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:\"python3 ./jail.py\",su=nobody"]
