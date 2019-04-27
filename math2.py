import random

def sum():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = a + b
    return [str(a) + " + " + str(b), c]
