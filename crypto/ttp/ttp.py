import random

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
key = ''.join(random.choice(alphabet) for i in range(1000))

with open("flag.txt", "r") as f:
    flag = f.read().strip()

def encrypt(data, key):
    encrypted = ""
    for i in range(len(data)):
        encrypted += chr(ord(data[i]) ^ ord(key[i]))
    return encrypted.encode("utf-8").hex()

enc_flag = encrypt(flag, key)
print(f"Encrypted flag: {enc_flag}")

data = "Haha! I heard xor prides perfect encryption, which you will never break!"
enc_data = encrypt(data, key)
print(f"Encrypted data: {enc_data}")
