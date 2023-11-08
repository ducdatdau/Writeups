from Crypto.Util.number import * 
from pwn import * 

p = remote("host3.dreamhack.games", 14005)

p.sendlineafter(b'[3] Get info\n', '3')
p.recvuntil(b'N: ')
N = int(p.recvline().strip().decode())
print('N = ', N)
p.recvuntil(b'e: ')
e = int(p.recvline().strip().decode())
print('e = ', e)
p.recvuntil(b'FLAG: ')
c = int(p.recvline().strip().decode())
print('c = ', c)

c1 = pow(2, e, N)
c2 = hex((c * c1) % N)

p.sendlineafter(b'[3] Get info\n', '2')
p.sendlineafter(b'(hex): ', str(c2)[2:])

m = int(p.recvline().strip()) // 2
print(long_to_bytes(m).decode())

p.interactive()

# DH{6623c33be90cc27728d4ec7287785992}