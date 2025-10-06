#!/usr/bin/env python3

from pwn import *

HOST = "actually-baby-rev.ctf.maplebacon.org"
PORT = 1337

p = remote(HOST, PORT)

payload1 = b'5' * 23 + b'999'
payload2 = b'4442'
payload3 = b'80673'
p.sendlineafter(b'> ', payload1)
p.sendlineafter(b'> ', payload2)
p.sendlineafter(b'> ', payload3)

p.interactive()

# maple{th3_b4by_cry1ng_1s_w0rs3_th4n_th1s_r3v3r51ng}