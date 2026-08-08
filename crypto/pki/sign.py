msg = input("Msg: ")
e = int(input("e: "))
n = int(input("n: "))

signature = pow(int.from_bytes(msg.encode(), 'big'), e, n)
print("Signature:", signature)
