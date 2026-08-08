with open("output.txt", "r") as f:
    enc_flag = f.readline().strip().split(": ")[1]
    enc_data = f.readline().strip().split(": ")[1]

def decrypt(data, key):
    data_unhex = bytes.fromhex(data).decode("utf-8")
    decrypted = ""
    for i in range(len(data_unhex)):
        decrypted += chr(ord(data_unhex[i]) ^ ord(key[i]))
    return decrypted

data = "Haha! I heard xor prides perfect encryption, which you will never break!"
key = decrypt(enc_data, data)
flag = decrypt(enc_flag, key)
print(f"Decrypted flag: {flag}")
