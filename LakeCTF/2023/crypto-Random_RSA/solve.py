from pwn import *
import random
from mt19937predictor import MT19937Predictor
from Crypto.Util.number import isPrime, long_to_bytes

predictor = MT19937Predictor()

while True:
    p = remote('chall.polygl0ts.ch', 9022)
    numbers = []

    while True:
        line = p.recvline().strip().decode()
        if 'Sadly, ' in line:
            x = int(line.split(' ')[1])
            numbers.append(x)
        else:
            c = int(line.split(' ')[1])
            break
    p.close()   
    if len(numbers) >= 624:
        break 
    
for i in range(624):
    x = numbers[i] 
    predictor.setrandbits(x, 1024)

while True:
    p = predictor.getrandbits(1024)
    if isPrime(p):
        break 

while True:
    q = predictor.getrandbits(1024)
    if isPrime(q):
        break

print('c =', c)
print('p =', p)
print('q =', q)

N = p * q 
phi = (p - 1) * (q - 1) 
e = 65537
d = pow(e, -1, phi)
m = pow(c, d, N)
print(m)

print(long_to_bytes(m).decode())

# EPFL{w0w_s0_much_r4nd000o0oo0om}