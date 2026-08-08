import random

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Public key format (encryption exponent, modulus)
known_keys = {
    "admin": (
        65537,
        21130487098389685933460965647196898393099978531051824491627170452840803549249897206307466673255228059000236806634634772810383364961086400464902271119049503112085201552201203373513938473085988542038803777599098910933005669975567263617846433168018435396064745650506281752187561958609638032383786861817056349588691394549769188201567330920256616661423179868316145355735317359885147414376857974066141790153056177495530772328656578152865326392800483985399744784141303772155334780712887730373623706972987373277115927128117816399526285770574250060233694654281053311213584445668651193705275941872402926242948276621112759628447,
    ),
    "guest": (
        3,
        20957646492463639745516416502795286082528506474474624278959425408406084204010614250646084776075562462170645676594472949276608908037854627894223580707465506892208473024780418599673191513834168384968439691914117704922784839041759230837926814828102435555232961422951742537360039004610882102097050432509205091173081233187106959307704661619832155652730518267417069111215612487084312958352530737784126891135727270202294436546755382527113748366702633595577228920002462500731648122262966026806739365640703669515811914535121509094783727746987089212029304646541795542927088093631786823518879944523533252814576325576831900186753,
    ),
}
username = None
key = known_keys["guest"]

with open("flag.txt", "r") as f:
    flag = f.read().strip()

def gen_random_string(length: int) -> str:
    return ''.join(random.choice(alphabet) for _ in range(length))

def rsa_sign(msg: str, d: int, n: int) -> int:
    msg_int = int.from_bytes(msg.encode(), 'big')
    signature = pow(msg_int, d, n)
    return signature

def rsa_verify(msg: str, signature: int, e: int, n: int) -> bool:
    msg_int = int.from_bytes(msg.encode(), 'big')
    verified_msg_int = pow(signature, e, n)
    return msg_int == verified_msg_int

def gen_challenge() -> str:
    return gen_random_string(32)

def choice_choose():
    global key
    username = input("Select by username (write no to use custom key): ")
    if username == "no":
        e = int(input("Enter public exponent (e): "))
        n = int(input("Enter modulus (n): "))
        key = (e, n)
        print("Custom key selected.")
    if username in known_keys:
        key = known_keys[username]
        print(f"Key for {username} selected.")
    else:
        print("Unknown username.")

def choice_verify():
    global key
    msg = input("Enter the message to verify: ")
    signature = int(input("Enter the signature: "))
    e, n = key
    if rsa_verify(msg, signature, e, n):
        print("Signature is valid.")
    else:
        print("Signature is invalid.")

def choice_login():
    global username
    global key
    for k, v in known_keys.items():
        if v[1] == key[1]:
            usr = k
            break
    else:
        print("No matching username found for the current key.")
        return

    challenge = gen_challenge()
    print(f"Sign this message to login: {challenge}")
    signature = int(input("Enter the signature: "))
    e, n = key
    if rsa_verify(challenge, signature, e, n):
        username = usr
        print(f"Login successful as {username}.")
    else:
        print("Login failed. Invalid signature.")

def main():
    print("Welcome to my personal PKI!")
    while True:
        print("1. Choose new key")
        print("2. Verify a message")
        print("3. Login")
        print("4. Exit")
        if username == "admin":
            print("5. Flag")
        choice = input("Enter your choice: ")

        if choice == "1":
            choice_choose()
        elif choice == "2":
            choice_verify()
        elif choice == "3":
            choice_login()
        elif choice == "4":
            print("Exiting...")
            break
        elif choice == "5":
            if username == None:
                print("You must login first.")
                continue
            if username != "admin":
                print("Access denied. You are not admin.")
                continue
            print(flag)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

