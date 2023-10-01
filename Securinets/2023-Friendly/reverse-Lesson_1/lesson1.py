# Difficulty: Easy
# follow me @ironbyte.tech

def encrypt(input):
    output = ""
    for i in range(len(input)):
        output += chr(ord(input[i]) + 2)
    return output


input = input("Enter a string to encrypt: ")
if (encrypt(input) == "j6emavj5arn5vj2t6a2ha5pet{rv32p"):
    print(f"Securinets{{{input}}}")
else:
    print("NO invalid flag !")
