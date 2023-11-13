from ptrlib import Socket
from hashlib import sha512
import ast


def h(m):
    return int(sha512(m.encode()).hexdigest(), 16)


sock = Socket("localhost", 10444)
p = int(sock.recvlineafter("p = "))
g = 2
w, v = ast.literal_eval(sock.recvlineafter("vkey = ").decode().strip())

magic_word = "cake_does_not_eat_cat"
m = h(magic_word)

# find one solution of aw - bv = m
a = 10
b = (a*w - m) * pow(v, -1, p-1) % (p-1)

s = pow(g, a, p)
t = pow(g, b, p)

sock.sendlineafter("erify: ", "V")
sock.sendlineafter("message: ", magic_word)
sock.sendlineafter("s: ", str(s))
sock.sendlineafter("t: ", str(t))

sock.interactive()
