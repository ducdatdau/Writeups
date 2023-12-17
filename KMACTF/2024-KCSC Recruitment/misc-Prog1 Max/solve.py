from pwn import *
import ast

p = remote("103.162.14.116", 14002)

for i in range(100):
    p.recvline()
    p.recvuntil(b'arr = ')
    arr = p.recvline().strip().decode()
    x = ast.literal_eval(arr)
    x.sort(reverse=True)
    p.sendlineafter(b'max =', str(x[0]))

p.interactive()
# KCSC{Ezzz_Programmingggg}