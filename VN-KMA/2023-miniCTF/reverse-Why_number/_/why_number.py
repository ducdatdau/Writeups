
flag = input("Give me the flag: ")
if len(flag) != 23: print("Incorrect lenght")

else:
    print("Correct lenght. Processing...")
    dest = [151, 154, 193, 220, 205, 220, 216, 156, 147, 205, 227, 226, 207, 149, 165, 209, 192, 205, 218, 227, 226, 234]
    correct = 1
    for i in range(22):
        if ord(flag[i]) + ord(flag[i+1]) != dest[i]:
            correct = 0
            break
    if correct: print("That's correct")
    else: print("Try again")

    