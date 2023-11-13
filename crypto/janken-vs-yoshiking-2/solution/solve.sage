from ptrlib import Socket
import ast
import re

sock = Socket("localhost", 10555)
_ = sock.recvline()
line = sock.recvline().decode()
p, M = re.findall(r"p: (\d+), and M: (.+)", line)[0]
p = int(p)
F = GF(p)
M = ast.literal_eval(M)
M = matrix(F, 5, 5, M)
o = M.det().multiplicative_order()


for _ in range(100):
    C = ast.literal_eval(sock.recvlineafter(r"commitment is=").decode())
    C = matrix(F, 5, 5, C)

    md = M.det()
    cd = C.det()
    x = discrete_log(cd, md)
    yoshiking_hand = x % 3
    hand = [3,1,2][yoshiking_hand]

    sock.sendlineafter("hand(1-3): ", str(hand))
    print(sock.recvlineafter("[system]").decode().strip())

sock.interactive()

