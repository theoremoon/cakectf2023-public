from ptrlib import Socket
from base64 import b64decode, b64encode
from hashlib import md5
from time import sleep

xor = lambda a, b: bytes([x^y for x, y in zip(a, b)])

def find_len():
    for i in range(16):
        sock = Socket("localhost", 10321)

        sock.sendlineafter(": ", "1")
        sock.sendlineafter("username(base64): ", b64encode(b"a"*i))
        cookie = sock.recvlineafter("cookie => ")
        cookie = b64decode(cookie)
        print(i, len(cookie))
        sock.close()
    return

# find_len()
# exit()

sock = Socket("localhost", 10321)
sock.sendlineafter(": ", "1")
username = b"a" * 9
sock.sendlineafter("username(base64): ", b64encode(username))

cookie = sock.recvlineafter("cookie => ")
cookie = b64decode(cookie)
blocks = [cookie[i:i+16] for i in range(0, len(cookie), 16)]
second = md5(blocks[1]).digest()
third = md5(blocks[2]).digest()

for c in range(256):
    payload = xor(second, bytes([c]) + b"|user=root|aaaa")
    payload = xor(third, payload)

    sock.sendlineafter(": ", "1")
    sock.sendlineafter("username(base64): ", b64encode(username + payload))
    
    payload_cookie = sock.recvlineafter("cookie => ")
    payload_cookie = b64decode(payload_cookie)

    attack_cookie = cookie[:32] + payload_cookie[48:]

    sock.sendlineafter(": ", "2")
    sock.sendlineafter("cookie: ", b64encode(attack_cookie))

    r = sock.recvline()
    if b"Hi, root!" in r:
        sock.interactive()
