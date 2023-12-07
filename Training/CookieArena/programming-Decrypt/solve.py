n = int(input())  
encoded_password = input() 

password = list(encoded_password)

divisors = []
def find_divisors(n):
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors
find_divisors(n)

for d in divisors:
    password[:d] = reversed(password[:d])  

decoded_password = ''.join(password)  

print(decoded_password)  

# CHH{pro9R4mmINg_D3CRYPT_394bf69578bbd9558bdaf3cce589050b}