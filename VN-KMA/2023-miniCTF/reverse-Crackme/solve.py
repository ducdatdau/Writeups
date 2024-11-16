secret_flag = "ardLRyTJNc8{VJE3O8M"

alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_"

def decode_secret(secret):

    rotate_const = 41

    decoded = ""

    for c in secret:
        index = alphabet.find(c)
        original_index = (index + rotate_const) % len(alphabet)
        decoded = decoded + alphabet[original_index]
    print(decoded)

decode_secret(secret_flag)

# CTF{3a5y_Enc7yti0n}