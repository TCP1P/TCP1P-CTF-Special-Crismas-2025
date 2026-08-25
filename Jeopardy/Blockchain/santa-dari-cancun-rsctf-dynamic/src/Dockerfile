FROM dimasmaualana/eth:latest@sha256:f9ee703e7da03d378d9a4fa70e00825e8a77593a29cf550dc7de5ede78f3ed58

ENV LAUNCHER_PORT=8080
ENV EVM_VERSION=cancun
EXPOSE 8080

# Each RSCTF container belongs to one team. One Gunicorn process with four
# threads keeps the launcher responsive without the upstream process overhead.
RUN grep -q -- '--workers 4' /startup/96-start-launcher \
    && grep -q -- '--threads 8' /startup/96-start-launcher \
    && sed -i 's/--workers 4/--workers 1/; s/--threads 8/--threads 4/' /startup/96-start-launcher

COPY deploy/ /home/ctf/
COPY *.sol /tmp/contracts/

RUN cd /tmp \
    && forge build --out /home/ctf/compiled \
    && rm -rf /tmp/contracts

USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN chmod 0555 /usr/local/bin/rsctf-entrypoint
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
CMD ["/entrypoint.sh"]
