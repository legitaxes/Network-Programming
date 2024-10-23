import random

def getLotto():
    return random.sample(range(1, 35), 7)

print(getLotto())