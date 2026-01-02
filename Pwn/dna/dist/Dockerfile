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

FROM openresty/openresty:jammy

# Install Runtime Dependencies (Tanpa build-essential/GCC)
RUN apt-get update && \
    apt-get install -y libsqlite3-dev sqlite3 luarocks && \
    rm -rf /var/lib/apt/lists/*

RUN luarocks install lsqlite3

# --- BAGIAN KUNCI ---
# Copy binary dna.so yang sudah jadi
COPY backend/extension/dna.so /usr/local/openresty/nginx/html/lib/dna.so

# Setup Lua & DB
WORKDIR /usr/local/openresty/nginx/html
COPY backend/src/ ./
COPY backend/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY backend/init_db.sql .

# Init DB
RUN sqlite3 market.db < init_db.sql
RUN chmod 777 market.db

# Copy Frontend
COPY --from=builder /app/dist /usr/local/openresty/nginx/html

EXPOSE 80
