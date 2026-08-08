from pwn import *
import ctypes

libc = ctypes.CDLL('/usr/lib/libc.so.6')
t = libc.time(0) // 60
t = t ^ 0xdeadbeef
libc.srand(t)
otp = libc.rand() % 10000
print(f"Generated OTP: {otp:04d}")

p = process('./main')
p.sendline(b"PTR je zakon!")
p.sendline(str(otp).encode())

p.interactive()
