import base64 

key = b'sTroN6PaSswORD'
base64_str = b'MBw6FDdZBT4wRzkQMB0jYEc8EUUDLQwjPiE8LR0TDw=='

bytesFlag = base64.b64decode(base64_str)

flag = ""
for i in range(len(bytesFlag)): 
    flag += chr(bytesFlag[i] ^ key[i % len(key)])

print(flag)

# CHH{yoU_c4N_bYP45S_sSL_PInninG}