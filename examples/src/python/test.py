def foo(a, b):
    if a > 2:
        return a
    elif b > 2:
        return b - a

    for i in range(a):
        b *= i

    return b

def bar(c):
    d = 1
    while c < 0:
        d += c
        d *= c
        c += 1

    return d
