local ffi = require("ffi")

-- Di dalam cdef, kita pakai syntax C, jadi // boleh dipakai di sini
ffi.cdef[[
    int dna_process_packet(const char* hex_input);
]]

-- TAPI DI LUAR CDEF ADALAH SYNTAX LUA.
-- Gunakan -- untuk komentar, bukan //
return ffi.load("/usr/local/openresty/nginx/html/lib/dna.so")
