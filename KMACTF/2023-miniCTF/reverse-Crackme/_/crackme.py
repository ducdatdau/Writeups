


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


def choose_greatest():

    value_1 = input("What's your first number? ")
    value_2 = input("What's your second number? ")
    if not (value_1.isnumeric() and value_2.isnumeric()):
        print("Invalid input")
    else:
        greatest_value = value_1
        if value_1 > value_2:
            greatest_value = value_1
        elif value_1 < value_2:
            greatest_value = value_2
        print("The number with largest positive magnitude is " + str(greatest_value))
        exit()

choose_greatest()

