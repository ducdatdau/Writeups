import random
import hashlib
from Crypto.Util.number import long_to_bytes

flag = ['amateursCTF{']
flag[0] += 'sn0h7YP'[::-1]

#  None[1][0] + input[1][1] - input[1][2] = 160 
# input[1][1] + input[1][2] - input[1][0] = 68
# input[1][2] + input[1][0] - input[1][1] = 34
# I guess None[1][0] = input[1][0]

# flag[1]
flag += [''.join(chr(i) for i in [97, 114, 51])]

# https://passwordrecovery.io/sha256
# flag[2]
flag += ['4']

random.seed(b'4')

part = [49, 89, 102, 109, 108, 52]
random.shuffle(part)

# [1, Y, f, m, l, 4]
# flag[3]
flag += ['f4m1lY']

# b'freebie' = b'0ffreebie'
# flag[4] 
flag += ['0f']

# flag[5]
# flag += [long_to_bytes(random.randint(0, 0xFFFFFFFF) ^ 0xFBFF4501)[::-1].decode() +
#          long_to_bytes(random.randint(0, 0xFFFFFFFF) ^  825199122)[::-1].decode() +
#          long_to_bytes(random.randint(0, 0xFFFFFFFF) ^ 0xFEEF2AA6)[::-1].decode()]

# Idk why I can't decode with utf8
# flag += ['N0Nv3nom0us']

flag += [ (random.randint(0, 0xFFFFFFFF) ^ 0xFBFF4501).to_bytes(4, 'little')  
        + (random.randint(0, 0xFFFFFFFF) ^  825199122).to_bytes(4, 'little')
        + (random.randint(0, 0xFFFFFFFF) ^ 0xFEEF2AA6).to_bytes(4, 'little')]
flag[5] = flag[5][:-1].decode()

# flag[6] 
x = 0x29ee69af2f3
y = ''

while x != 0:
    y += chr(x % 128)
    x //= 128

flag += [y[::-1]]
flag = '_'.join(i for i in flag)
flag += '}'

print(flag)

# amateursCTF{PY7h0ns_ar3_4_f4m1lY_0f_N0Nv3nom0us_Sn4kes}