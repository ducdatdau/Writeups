from z3 import *

solver = Solver()

flag = [Int(f'flag[{i}]') for i in range(36)]

for i in range(36):
    solver.add(flag[i] >= 0, flag[i] <= 128)

solver.add(flag[0] == ord('I'))
solver.add(flag[1] == ord('S'))
solver.add(flag[2] == ord('I'))
solver.add(flag[3] == ord('T'))
solver.add(flag[4] == ord('D'))
solver.add(flag[5] == ord('T'))
solver.add(flag[6] == ord('U'))
solver.add(flag[7] == ord('{'))
solver.add(flag[8] == 0x61)
solver.add(flag[17] == 0x63)
solver.add(flag[18] == 0x61)
solver.add(flag[19] == 0x74)
solver.add(flag[33] == flag[34])
solver.add(flag[35] == ord('}'))

solver.add(flag[22] + flag[3] + flag[18] * flag[9] * flag[21] - flag[6] == 451644)
solver.add(flag[24] + flag[35] + flag[17] - flag[19] - flag[26] - flag[6] == 27)
solver.add(flag[8] * flag[1] + flag[32] * flag[27] * flag[25] - flag[29] == 0x83872)
solver.add(flag[7] + flag[20] * flag[10] * flag[4] - flag[6] - flag[11] == 665370)
solver.add(flag[14] + (flag[16] - 1) * flag[31] - flag[30] * flag[22] == -2945)
solver.add(flag[33] + flag[3] - flag[9] - flag[18] - flag[11] - flag[4] == -191)
solver.add(flag[1] + flag[30] + flag[18] + flag[25] * flag[29] - flag[8] == 4853)
solver.add(flag[13] + flag[5] - flag[7] * flag[14] * flag[23] * flag[2] == -86153321)
solver.add(flag[13] + flag[9] * flag[5] * flag[12] + flag[27] * flag[10] == 873682)
solver.add(flag[21] + flag[34] + flag[24] + flag[32] * flag[23] - flag[4] == 9350)
solver.add(flag[14] + flag[13] + flag[15] + flag[23] * flag[19] - flag[3] == 11247)
solver.add(flag[2] + flag[17] + flag[7] * flag[12] - flag[15] - flag[21] == 13297)
solver.add(flag[8] + flag[35] + flag[26] + flag[28] - flag[0] - flag[20] == 266)
solver.add(flag[2] + flag[17] + flag[0] + flag[12] * flag[28] - flag[1] == 10422)
solver.add(flag[22] + flag[15] + flag[5] * flag[19] - flag[34] - flag[11] == 9883)
solver.add(flag[10] * flag[33] + flag[16] * (1 - flag[20]) - flag[0] == -5604)

if solver.check() == sat:
    model = solver.model()
    print(model)
else:
    print("No solution found.")

flag[0] = 73
flag[1] = 83
flag[2] = 73
flag[3] = 84
flag[4] = 68
flag[5] = 84
flag[6] = 85
flag[7] = 123
flag[8] = 97
flag[17] = 99
flag[18] = 97
flag[19] = 116
flag[35] = 125
flag[33] = 33
flag[13] = 100
flag[12] = 108
flag[26] = 117
flag[22] = 110
flag[21] = 49
flag[20] = 95
flag[27] = 114
flag[23] = 95
flag[29] = 97
flag[10] = 103
flag[11] = 48
flag[32] = 97
flag[15] = 110
flag[31] = 101
flag[16] = 95
flag[30] = 114
flag[9] = 95
flag[14] = 101
flag[28] = 95
flag[25] = 48
flag[34] = 33
flag[24] = 121

# print("".join([chr(i) for i in flag]))
# ISITDTU{a_g0lden_cat_1n_y0ur_area!!}