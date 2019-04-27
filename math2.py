import random

def sum():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = a + b
    return [str(a) + " + " + str(b), c]

def raznost():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = a + b
    return [str(c) + " - " + str(a), b]

def multiply():
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    c = a * b
    return [str(a) + " * " + str(b), c]

def delenie():
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    c = a * b
    return [str(c) + " / " + str(a), b]

def vibor():
    x = random.randint(0, 4)
    if x == 0:
        return sum()
    elif x == 1:
        return raznost()
    elif x == 2:
        return multiply()
    else:
        return delenie()
