import math
d = {i: math.sqrt(i) for i in range(1, 101)}

c = 0 
for i in d.items():
    if c < 4: 
        print(i)
    c += 1  