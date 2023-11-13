key = 0x223620
flag = b"CakeCTF{wow_you_know_a_lot_of_animals}"

for i in range(len(flag) - 4):
    v = int.from_bytes(flag[i:i+4], 'little')
    v ^= key
    key += 0x3776
    flag = flag[:i] + int.to_bytes(v, 4, 'little') + flag[i+4:]

print(list(flag))
print(len(flag))

key = 0x223620

for i in range(len(flag) - 4):
    v = int.from_bytes(flag[i:i+4], 'little')
    v ^= key
    key += 0x3776
    flag = flag[:i] + int.to_bytes(v, 4, 'little') + flag[i+4:]

print(flag)
