#Calcolo delle operazioni essenziali con i matrici e vettori
#Computing essential operations with matrixes and vectors
#Wesentliche Operationen mit Matrizen und Vektoren berechnen

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


#Dot product
 
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

#print(matrixC)        

#With nested list comprehension

m_C = [[]]