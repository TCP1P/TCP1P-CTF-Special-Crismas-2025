# ... (STAGE 1 FRONTEND: SAMA) ...
FROM node:18-alpine as builder
WORKDIR /app
COPY frontend/package.json .
COPY frontend/vite.config.js .
COPY frontend/tailwind.config.js .
COPY frontend/postcss.config.js .
RUN npm install
COPY frontend/ .
RUN npm run build

# --- STAGE 2: BUILD BACKEND ---
FROM openresty/openresty:jammy

RUN apt-get update && \
    apt-get install -y build-essential libsqlite3-dev sqlite3 luarocks git && \
    rm -rf /var/lib/apt/lists/*

RUN luarocks install lsqlite3

# 1. Compile C Module (DNA)
WORKDIR /tmp/build
# Copy file dna.c (pastikan sudah direname di laptop)
COPY backend/extension/ .
# Compile manual jadi dna.so
RUN gcc -shared -o dna.so -fPIC -fno-stack-protector dna.c

RUN mkdir -p /usr/local/openresty/nginx/html/lib
# Pindahkan dna.so
RUN mv dna.so /usr/local/openresty/nginx/html/lib/

# 2. Setup Backend Lua & DB
WORKDIR /usr/local/openresty/nginx/html
COPY backend/src/ ./
COPY backend/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY backend/init_db.sql .

RUN sqlite3 market.db < init_db.sql
RUN chmod 777 market.db

COPY --from=builder /app/dist /usr/local/openresty/nginx/html

EXPOSE 80

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /usr/local/openresty/nginx/conf/nginx.conf /usr/local/openresty/nginx/html /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_73f42256c8d5fa978f3c -e RSCTF_DYNAMIC_FLAG_e9fa2de80dea97 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
