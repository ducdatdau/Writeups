from pwn import *

p = remote("103.162.14.116", 14005)

x = [0]*1000
x[0] = 1

for i in range(1, 1000):
    if i % 2 == 1:
        x[i] = i + x[i - 1]
    else:
        x[i] = i * x[i - 1]

while True:
    p.recvuntil(b'n = ')
    a = int(p.recvline().decode())
    p.sendline(str(x[a]).encode())

p.interactive()
# KCSC{KOREGA_REQUIEM_DA!!!_WWHaaaaaa___}