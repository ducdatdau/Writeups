x = 100000
y = 1000000

for i in range(10000): 
    x *= (1.68/100 + 1)
    print(i, x)
    if (x >= y):
        break

