from timer import Timer
import http.client, json, os
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
    print('los gehts!')
    return(matrix)

def funfact():
    conn = http.client.HTTPSConnection('numbersapi.p.rapidapi.com')

    headers = {
        'X-RapidAPI-Key': 'f26fbfc3c5msh0ed852bd7999cdbp14fd28jsnec2403b96d20',
        'X-RapidAPI-Host': 'numbersapi.p.rapidapi.com'
    }

    randint = random.randint(0,200)
    conn.request("GET", f"/{randint}/math?fragment=true&json=true", headers=headers)
    response = conn.getresponse()
    data = response.read()
    js = json.loads(data)
    return {str(js['number']): js['text']}

def construct_matrix(model_matrix):
    m = model_matrix()
    def fill_with_messages():
        random_messages = [
        'Geben Sie bitte ein Primzahl',
        'Noch ein Primzahl!',
        'Grosser Auswahlen!',
        'Schrifft fur Schrifft...',
        'Gut getan!',
        'Wunderbar'
        ]
        
        for i in range(len(m)):
            for j in range(len(m[0])):
                while True:
                    os.system('cls')
                    message = random_messages[random.randint(0,(len(random_messages)-1))]
                    n = (input('\n'))
                    try:
                        n = int(n)
                        if not isprime(n):
                            print('Kein Primzahl!')
                            continue
                        print(message)
                        break
                    except:
                        print('Ungultiges Datei!')
                        continue
                    
                m[i][j] = n
                print(np.array(m))
            fact = funfact()
            n = [j for j in fact.keys()]
            f = fact[str(n[0])]
            print(n, f)
    return fill_with_messages





def run():
    constructed = construct_matrix(model_matrix)
    constructed()



    


if __name__=='__main__':
    run()