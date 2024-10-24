def fibonacci(n):
    # generate until n
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b
    

for i in fibonacci(1000000):
    print(i)
    
