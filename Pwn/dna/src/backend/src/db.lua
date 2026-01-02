local sqlite3 = require("lsqlite3")

local _M = {}
local db_path = "/usr/local/openresty/nginx/html/market.db"

function _M.get_db()
    local db = sqlite3.open(db_path)
    if not db then
        ngx.log(ngx.ERR, "[DB] Failed to open DB")
        return nil
    end
    return db
end

function _M.get_products()
    local db = _M.get_db()
    if not db then return {} end

    -- Ambil semua produk
    local stmt = db:prepare("SELECT * FROM products")
    local rows = {}

    if stmt then
        while stmt:step() == sqlite3.ROW do
            local row = stmt:get_named_values()
            table.insert(rows, row)
        end
        stmt:finalize()
    else
        ngx.log(ngx.ERR, "[DB] Error preparing product query: " .. db:errmsg())
    end

    db:close()
    return rows
end

function _M.get_flag()
    local db = _M.get_db()
    if not db then return "DB_CONNECTION_ERROR" end

    -- UPDATE DISINI: Sesuaikan dengan tabel 'secrets'
    local stmt = db:prepare("SELECT data FROM secrets WHERE owner='admin' LIMIT 1")
    local flag = "flag not found"

    if stmt then
        if stmt:step() == sqlite3.ROW then
            -- Ambil kolom ke-0 (yaitu 'data')
            flag = stmt:get_value(0)
        end
        stmt:finalize()
    else
        ngx.log(ngx.ERR, "[DB] Error preparing flag query: " .. db:errmsg())
    end

    db:close()
    return flag
end

return _M
