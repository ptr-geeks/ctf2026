from pwn import *

with open("output.txt", "r") as f:
    flag = f.read().strip().encode()
current = flag
while True:
    p = process("./main")
    p.sendline(current)
    current = p.recvline().strip()
    p.close()
    if current == flag:
        break
    print(">>>", current)
