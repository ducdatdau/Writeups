X = [0x0AD, 0x0D8, 0x0CB, 0x0CB, 0x9D, 0x97, 0x0CB, 0x0C4, 0x92, 0x0A1, 0x0D2, 0x0D7, 0x0D2, 0x0D6, 0x0A8, 0x0A5, 0x0DC, 0x0C7, 0x0AD, 0x0A3, 0x0A1, 0x98, 0x4C, 0x0]

# F[0] + F[1] = X[0] 
# F[1] + F[2] = X[1]

# F[21] + F[22] = X[21]
# F[22] + F[23] = X[22]
# F[23] + F[24] = X[23]

F = [0] * 25

# There are two cases F[22] = i or F[23] = i 

for i in range(33, 127):
    F[22] = i
    F[23] = 76 - F[22] 
    # F[24] = X[23] - F[23]

    for i in range(21, -1, -1):
        F[i] = X[i] - F[i + 1]
    
    flag = ''
    for i in range(24):
        flag += chr(F[i])
    print(flag)

# DH{All_l1fe_3nds_w1th_NULL}