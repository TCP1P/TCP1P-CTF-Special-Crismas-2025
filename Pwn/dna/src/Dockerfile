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
