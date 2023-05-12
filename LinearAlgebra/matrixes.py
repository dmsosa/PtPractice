import numpy as np

#Calcolo delle operazioni essenziali con i matrici e vettori
#Computing essential operations with matrixes and vectors
#Wesentliche Operationen mit Matrizen und Vektoren berechnen

#////////////////////////////////////////////////

    #Sum

SumA = [[1,2,3],
        [4,5,6],
        [7,8,9]]

SumB = [[1,2,3],
        [1,1,1],
        [-1,-1,-1]]

Result_Sum_C = list()

for i in range(len(SumA)):
    row_result = list()
    for j in range(len(SumA[0])):
        result = SumA[i][j] + SumB[i][j]
        row_result.append(result)
    Result_Sum_C.append(row_result)

#print(Result_Sum_C)

        #With list-comprenhension

sumC = [[SumA[i][j] + SumB[i][j] for j in range(len(SumA[0]))] for i in range(len(SumA))]
#print(sumC)

#////////////////////////////////////////////////

    #Matrizen Multiplication

    #Scalar Multiplication (dot product) with Numpy

dotA = [[2,4],
     [3,6]]

dotB = np.dot(dotA, 5)
# print(B)

    #Matrix Multiplication with Numpy

matmulA = [[2,3,5],
     [4,5,7]]

matmulB = [[1, 0],
     [0, 1],
     [5, 5]]

matmulC = np.matmul(matmulA,matmulB)
# print(C [1,1])

    #Wise Multiplication

wiseA = np.array([[1, 2, 3], [9, 8 ,5]])
wiseB = np.array([[28, 37, 45], [12, 14, 17]])

wiseC = np.multiply(wiseA, wiseB)
# print(wiseC)

wiseC1 = np.multiply(wiseA[0, :], wiseB[1, :])
wiseC2 = np.multiply(wiseA[1, :], wiseB[0, :])

# print(wiseC1)
# print(wiseC2)
wiseC3 = [wiseC1, wiseC2]

result = np.array(wiseC3)
# print(result [1,2])

        #With lists
matrixA = [[12, 7, 3],
    [4, 5, 6],
    [7, 8, 9]]

matrixB = [[5,8,1],
    [6,7,3],
    [4,5,9]]    

matrixC = [[0,0,0],
           [0,0,0],
           [0,0,0]]

for i in range(len(matrixA)):
    for j in range(len(matrixB[0])):
        for k in range(len(matrixB)):
            matrixC[i][j] += matrixA[i][k] * matrixB[k][j]

# print(matrixC)        

        #With nested list comprehension

m_C = [[sum (x*y for x,y in zip(mA_row, mB_col)) for mB_col in zip(*matrixB)] for mA_row in matrixA]

# for result in m_C:
#     print(result)

#////////////////////////////////////////////////

    #Transposing a matrix!

m = [[9,8,7],
     [6,5,4],
     [3,2,1]]

        #With nested list comprehension
mT = [[m[j][i] for j in range(len(m[0]))] for i in range(len(m))]

# print(mT)

    #Interchanging two rows

intA = [[2, 3, 1],
        [4, 5, 9],
        [7, 6, 8]]

        #Classic method

def Swap(mat, posA, posB): #This function interchanges the positions of posA and posB given as arguments.
    row = len(mat)
    col = len(mat[0])

    for j in range(col):
        aux = mat[posA][j]
        mat[posA][j] = mat[posB][j]
        mat[posB][j] = aux

# Swap(intA, 0, 2)
# print(intA)

        #Without function
    
cloneA = intA

cloneA[1], cloneA[2] = cloneA[2], cloneA[1]
# print(cloneA)

#Solving Linear Equations

E = np.array([[2, -1, 5],
     [1, 2, 5],
     [0, 1, 0]])
F = np.array([3, 4, 5])

X = np.linalg.inv(E).dot(F)
# print(X)

mE = np.array([[2, -1],
      [1, 1]])
mF =  np.array([3, 5])

mX = np.linalg.solve(mE, mF)
# print(mX)

    #With numpy

archA = np.matrix([[1,1,0],
                   [0,-1,1],
                   [0,-2,2]])

archA2 = np.array([[3,4,6]])
archB = np.array([[5,6,7]])

C = 2*archB
print(C)