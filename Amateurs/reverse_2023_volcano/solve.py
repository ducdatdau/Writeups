from pwn import *

HOST = "amt.rs" 
PORT = 31010

r = remote(HOST, PORT)

# I don't use the Chinese Remainder Theorem because I'm so bad at math. 
def count_set_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

for i in range(131072, 18446744073709551615):
    if i % 2 == 0 and i % 3 == 2 and i % 5 == 1 and i % 7 == 3 and i % 109 == 55 and count_set_bits(i) >= 17 and count_set_bits(i) <= 26:
        key = i
        break

# 1048526

r.sendlineafter(b'bear: ', b'1048526')
r.sendlineafter(b'volcano: ', b'1048526')
r.sendlineafter(b'same: ', b'11')

r.interactive()

# amateursCTF{yep_th0se_l00k_th3_s4me_to_m3!_:clueless:}