from ptrlib import *
from PIL import Image
from tqdm import tqdm
import hashlib

img = Image.new('1', (480, 20), 'white')

md5s = []
with open("../distfiles/imgchk", "rb") as f:
    for x in range(480):
        f.seek(0x6020 + x*8)
        offset = u64(f.read(8))
        f.seek(offset)
        md5s.append(f.read(16))

known = {}
for x in tqdm(range(480)):
    if md5s[x] in known:
        v = known[md5s[x]]
        for i in range(20):
            img.putpixel((x, i), (v >> i) & 1)
        continue

    for v in range((1<<20)-1, -1, -1):
        h = hashlib.md5(int.to_bytes(v, 3, 'little')).digest()
        if h == md5s[x]:
            known[md5s[x]] = v
            for i in range(20):
                img.putpixel((x, i), (v >> i) & 1)
            break

img.save("output.png")

    
