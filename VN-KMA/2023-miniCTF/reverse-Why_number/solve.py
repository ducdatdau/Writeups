x = [151, 154, 193, 220, 205, 220, 216, 156, 147, 205, 227, 226, 207, 149, 165, 209, 192, 205, 218, 227, 226, 234]

flag = 'C'
for i in range(len(x)):
    flag += chr(x[i] - ord(flag[i]))

print(flag)

# CTF{alph4_numb3r_alnum}