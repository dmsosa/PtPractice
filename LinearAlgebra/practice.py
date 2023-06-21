

def decorator(func):
    import math
    def feat(n):
        r = func(n)
        return r, math.sqrt(r)
    return feat


@decorator
def f(n):
    return 2*n

p, r = f(5)
print(p, r)