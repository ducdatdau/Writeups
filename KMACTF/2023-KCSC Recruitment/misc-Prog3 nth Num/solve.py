from pwn import * 

def cal(k):
    n = 1
    d = 1

    while k > 9 * n * d:
        k -= 9 * n * d
        n *= 10
        d += 1

    x = str(n + (k - 1) // d)
    x = list(x)
    return (x[(k - 1) % d])

p = remote("103.162.14.116", 14004)
p.recvuntil(b'-> Output: 3')

while True:
    p.recvuntil(b'n = ')
    k = int(p.recvline().decode().strip())
    p.sendlineafter(b'>> ', str(cal(k)).encode())

p.interactive()
# KCSC{dO_yOu_knOw_prOgrAmmIng_Is_vErY_ImpOrtAnt?}