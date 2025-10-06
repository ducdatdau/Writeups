from z3 import * 

solver = Solver()
flag = [BitVec(f'flag[{i}]', 8) for i in range(16)]

for i in range(16):
    solver.add(Or((flag[i] == ord('t')), (flag[i] == ord('u')), (flag[i] == ord('a')), (flag[i] == ord('n')), (flag[i] == ord('l')), (flag[i] == ord('i')), (flag[i] == ord('h'))))

solver.add(flag[0] + flag[1] + flag[2] == 0x4A)
solver.add(flag[1] + flag[2] + flag[3] == 0x44)
solver.add(flag[2] + flag[3] + flag[4] == 0x3B)
solver.add(flag[3] + flag[4] + flag[5] == 0x43)
solver.add(flag[4] + flag[5] + flag[6] == 0x43)
solver.add(flag[5] + flag[6] + flag[7] == 0x3F)
solver.add(flag[6] + flag[7] + flag[8] == 0x42)
solver.add(flag[7] + flag[8] + flag[9] == 0x3D)
solver.add(flag[8] + flag[9] + flag[10] == 0x43)
solver.add(flag[9] + flag[10] + flag[11] == 0x3F)
solver.add(flag[10] + flag[11] + flag[12] == 0x4A)
solver.add(flag[11] + flag[12] + flag[13] == 0x51)
solver.add(flag[12] + flag[13] + flag[14] == 0x4A)
solver.add(flag[13] + flag[14] + flag[15] == 0x44)

if solver.check() == sat:
    model = solver.model()
    res = ""
    for i in range(16):
        res += chr(model[flag[i]].as_long())
    print(res)
else:
    print("......")