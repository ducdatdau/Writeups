import string
import random

alphabet = string.ascii_letters + string.digits + "!{_}?"
ct = 'ldtdMdEQ8F7NC8Nd1F88CSF1NF3TNdBB1O'

flag = ""
for i in ct:
    for j in alphabet:
        if alphabet.index(i) == (alphabet.index(j) + 42) % 67:
            flag += j
print(flag)
# KCSC{C3as4r_1s_Cl4ss1c4l_4nd_C00l}