local cjson = require("cjson")
local db = require("db")
-- Ubah require
local dna = require("dna")

local _M = {}

function _M.handle()
    ngx.header.content_type = "application/json"
    local uri = ngx.var.uri
    ngx.req.read_body()
    local body_str = ngx.req.get_body_data()
    local body = {}
    if body_str then pcall(function() body = cjson.decode(body_str) end) end

    if uri == "/api/shop/items" then
        ngx.say(cjson.encode(db.get_products()))
        return
    end

    if uri == "/api/user/secure_update" then
        local packet = body.packet or ""

        -- Panggil fungsi baru: dna_process_packet
        local result_role = dna.dna_process_packet(packet)

        local response = {
            role = result_role,
            msg = "Sequence Processed" -- Ubah pesan biar tema DNA
        }

        if result_role == 322420958 then -- 0x1337C0DE
            response.msg = "ACCESS GRANTED: GENOME UNLOCKED"
            response.flag = db.get_flag()
        else
            response.msg = "Sequence Rejected: Integrity Verification Failed"
        end

        ngx.say(cjson.encode(response))
        return
    end
end
return _M
