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

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in / /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_323d8 -e RSCTF_DYNAMIC_FLAG {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
