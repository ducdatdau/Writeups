import string
import random

alphabet_string = string.ascii_letters + string.digits + "!{_}?"
ct = '2V9VnRcNosvgMo4RoVfThg8osNjo0G}mmqmp'

for i1 in range(0, 65):
    for i2 in range(i1 + 1, 66):
        for i3 in range(i2 + 1, 67):
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '{', '_', '}', '?']
            alphabet[i1] = alphabet[i2] = alphabet[i3] = ''
            alphabet = "".join(alphabet)

            ok = 1
            for i in ct:
                if not i in alphabet:
                    ok = 0
                    break
            if ok == False:
                continue

            if not 'K' in alphabet:
                continue
            if not 'C' in alphabet:
                continue
            if not 'S' in alphabet:
                continue
            if not '{' in alphabet:
                continue
            if not '}' in alphabet:
                continue
  
            for k in range(64):
                if alphabet[(alphabet.index('K') + k) % 64] == '2' and alphabet[(alphabet.index('C') + k) % 64] == 'V' and alphabet[(alphabet.index('S') + k) % 64] == '9' and alphabet[(alphabet.index('{') + k) % 64] == 'n':
                    cnt += 1

                    flag = ""
                    for i in ct:
                        for j in alphabet:
                            if alphabet.index(i) == (alphabet.index(j) + k) % 64:
                                flag += j
                    print(flag, k, alphabet)