import math
d = {i: math.sqrt(i) for i in range(1, 101) if i%3 != 0}

pri = lambda it:print(it)
pri(d)