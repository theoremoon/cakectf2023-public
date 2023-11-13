from ptrlib import Socket
from hashlib import sha256
from Crypto.Util.number import long_to_bytes, inverse
import secrets


def h1(s: bytes) -> int:
    return int(sha256(s).hexdigest()[:40], 16)

def h2(s: bytes) -> int:
    return int(sha256(s).hexdigest()[:50], 16)


g = 3
def sign(m: bytes):
    z = h1(m)
    k = inverse(h2(long_to_bytes(x + z)), q)
    r = h2(long_to_bytes(pow(g, k, p)))
    s = (z + x*r) * inverse(k, q) % q
    return r, s

q = 10855513673631576111128223823852736449477157478532599346149798456480046295301804051241065889011325365880913306008412551904076052471122611452376081547036735239632288113679547636623259366213606049138707852292092112050063109859313962494299170083993779092369158943914238361319111011578572373690710592496259566364509116075924022901254475268634373605622622819175188430725220937505841972729299849489897919215186283271358563435213401606699495614442883722640159518278016175412036195925520819094170566201390405214956943009778470165405468498916560026056350145271115393499136665394120928021623404456783443510225848755994295718931
p = 2*q + 1

sock = Socket("localhost", 9999)

salt = sock.recvlineafter("salt = ").decode().strip()
salt = bytes.fromhex(salt)
y = int(sock.recvlineafter("y = "))

n = 20

ms = []
ss = []
for _ in range(n):
    m = secrets.token_hex(10)
    sock.sendlineafter("erify:", "s")
    sock.sendlineafter("m = ", m)
    s = int(sock.recvlineafter("s = "))

    ms.append(m)
    ss.append(s)

# let l[i] = k[i]^{-1}
# 
# find coefficients (r[i]*l[i], r[j]*l[j]) for equations
#  s[j]*(r[i]*l[i]) - s[i]*(r[j]*l[j]) = <small>
#
ZK = 2**360  # upper bound of z*l
# v = (r0*l0, r1*l1, ..., t0, t1, ...)
M = block_matrix([
    [ZK, matrix(ZZ, 1, n-1, ss[1:]), 0],
    [0, matrix.identity(n-1) * ss[0], 0],
    [0, matrix.identity(n-1) * q, matrix.identity(n-1)],
])

L = M.LLL()
v = L[0] * M**(-1)

lr = [abs(int(v[i])) for i in range(n)] 

# Solve HNP s[i] = z[i]*l[i] + l[i]*r[i]*x mod q
# for z[i]*l[i] and x
#
# v2 = (t1, t2, ..., x, 1)
M2 = block_matrix([
    [matrix.identity(n) * q,     0,  0],
    [matrix(QQ, 1, n, lr), ZK/q,  0],
    [matrix(QQ, 1, n, ss),       0, ZK],
])
L2 = M2.LLL()
v2 = L2[1] * M2**(-1)
x = abs(int(v2[-2]))

# sometimes this may fail
assert y == pow(g, x, p)

m2 = b"hirake goma"
r2, s2 = sign(m2 + salt)

sock.sendlineafter("erify:", "v")
sock.sendlineafter("m = ", m2)
sock.sendlineafter("r = ", str(r2))
sock.sendlineafter("s = ", str(s2))

print(sock.recvline())
