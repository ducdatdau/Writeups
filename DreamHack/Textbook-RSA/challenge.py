#!/usr/bin/python3
from Crypto.Util.number import getStrongPrime, bytes_to_long, inverse


class RSA(object):
    def __init__(self):
        self.p = getStrongPrime(512)
        self.q = getStrongPrime(512)
        self.N = self.p * self.q
        self.e = 0x10001
        self.d = inverse(self.e, self.N - self.p - self.q + 1)

    def encrypt(self, pt):
        return pow(pt, self.e, self.N)

    def decrypt(self, ct):
        return pow(ct, self.d, self.N)


rsa = RSA()
FLAG = bytes_to_long(open("flag", "rb").read())
FLAG_enc = rsa.encrypt(FLAG)

print("Welcome to dream's RSA server")

while True:
    print("[1] Encrypt")
    print("[2] Decrypt")
    print("[3] Get info")

    choice = input()

    if choice == "1":
        print("Input plaintext (hex): ", end="")
        pt = bytes_to_long(bytes.fromhex(input()))
        print(rsa.encrypt(pt))

    elif choice == "2":
        print("Input ciphertext (hex): ", end="")
        ct = bytes_to_long(bytes.fromhex(input()))
        if ct == FLAG_enc or ct > rsa.N:
            print("Do not cheat !")
        else:
            print(rsa.decrypt(ct))

    elif choice == "3":
        print(f"N: {rsa.N}")
        print(f"e: {rsa.e}")
        print(f"FLAG: {FLAG_enc}")

    else:
        print("Nope")
