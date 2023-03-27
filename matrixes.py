A = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]


B = [[A[j][i] for j in range(len(A[0]))] for i in range(len(A))]

for x in B:
    print(x,end="\n")
