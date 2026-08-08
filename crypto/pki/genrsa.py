from cryptography.hazmat.primitives.asymmetric import rsa



private_key = rsa.generate_private_key(
    public_exponent=3,
    key_size=2048,
)

public_key = private_key.public_key()

print("e:", public_key.public_numbers().e)
print("n:", public_key.public_numbers().n)
print("d:", private_key.private_numbers().d)
