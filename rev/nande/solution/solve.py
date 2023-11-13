with open("../distfiles/nand.exe", "rb") as f:
    f.seek(0x0001c600)
    seq = list(f.read(0x100))

for _ in range(0x1234):
    seq[0xff] ^= 1
    for i in range(0xfe, -1, -1):
        seq[i] ^= seq[i+1]

flag = ""
for i in range(0, 0x100, 8):
    c = 0
    for j in range(8):
        c |= seq[i+j] << j
    flag += chr(c)

print(flag)
