from pwn import *

p = remote("103.162.14.116", 14003)
def isValidParentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)

    return not stack


p.recvuntil(b'I will give you the flag after 100 rounds :D')

while True:
    p.recvuntil(b': ')
    string = p.recvline().decode().strip()
    if isValidParentheses(string): 
        res = b'yes'
    else:
        res = b'no'
    p.sendlineafter(b'yes/no?: ', res)


p.interactive()
# KCSC{Smile_Emoji____:)___}