DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS secrets; -- Ganti flag jadi secrets

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER,
    desc TEXT,
    image TEXT
);

CREATE TABLE secrets (
    id INTEGER PRIMARY KEY,
    owner TEXT,
    data TEXT
);

INSERT INTO products (name, price, desc, image) VALUES
('Zero-Day Kernel Exploit', 5000, 'Unpatched local privilege escalation.', '💀'),
('Ghost VPN Access', 200, 'No logs, pure anonymity.', '🛡️'),
('Corporate DB Dump', 1500, 'Fortune 500 employee records.', '💽'),
('Satellite Uplink Key', 99999, 'Direct military downlink.', '📡');

INSERT INTO secrets (owner, data) VALUES ('admin', 'XMAS{akumaujadifulstakkkkkkkkkdevloper}');
