from timer import Timer
import threading
import math, random
import numpy as np

def isprime(n: int) -> bool:
    if n <= 3:
        return n > 1
    elif n % 2 == 0 or n % 3 == 0:
        return False
    else:
        root = math.floor(math.sqrt(n))
        for i in range(5, root, 6):
            if n % i == 0:
                return False
    return True

def model_matrix():
    while True:
        m = input('Hallo! Auswahlen Sie wie viele Reihen\n')
        n = input('und wie viele Spalten?\n')
        try:
            m = int(m)
            n = int(n)
            break
        except:
            print('Geben Sie bitte gultigen Zahlen!')
            continue
        
    matrix = []
    for i in range(0,m):
        row = []
        for j in range(0,n):
            row.append(0)
        matrix.append(row)
    return(matrix)

def construct_matrix(matrix):
    random_messages = [
        'Geben Sie bitte ein Primzahl',
        'Noch ein Primzahl!',
        'Grosser Auswahlen!',
        'Schrifft fur Schrifft...',
        'Gut getan!',
        'Wunderbar'
    ]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            while True:
                message = random_messages[random.randint(0,(len(random_messages)-1))]
                n = (input(f'{message}\n'))
                try:
                    n = int(n)
                except:
                    print('Ungultiges Datei!')
                    continue
                if not isprime(n):
                    print('Kein Primzahl!')
                    continue
                break
            matrix[i][j] = n
            print(np.array(matrix))
            print('FunFact\n')

def funfact():
    pass

def run():
    
    M = model_matrix()
    construct_matrix(M)

    


if __name__=='__main__':
    run()