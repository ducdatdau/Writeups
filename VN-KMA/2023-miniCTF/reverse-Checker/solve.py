flag = ['z'] * 50 
flag[21] = "1"
flag[1]  = "T"
flag[22] = "n"
flag[0]  = "C"
flag[19] = "r"
flag[24] = "}"
flag[16] = "3"
flag[23] = "g"
flag[3]  = "{"
flag[15] = "R"
flag[13] = "0"
flag[6]  = "l"
flag[9]  = "m"
flag[4]  = "W"
flag[11] = "_"
flag[14] = "_"
flag[18] = "3"
flag[20] = "5"
flag[7]  = "c"
flag[2]  = "F"
flag[8]  = "o"
flag[5]  = "e"
flag[17] = "v"
flag[10] = "e"
flag[12] = "t"

res = ''
for i in range(len(flag)): 
    res += flag[i]

print(res)

# CTF{Welcome_t0_R3v3r51ng}