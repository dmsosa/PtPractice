import math, random, os
def getwort():
    with open("./data.txt", "r") as f:
        worter = f.read().split("\n")
        rand = math.floor(random.random()*(len(worter)))
        wort = worter[rand].upper()
        return wort

def arbeit(wort):
    print(wort)
    j = list()
    dic = {k:[i for i in range(len(wort)) if wort[i] == k] for k in wort}
    print(dic)
    return dic

def check(rat, dic, response):
    new_response = []
    indexes = []
    for i in response:
        new_response.append(i)
    if rat in dic.keys():
        indexes = dic.get(rat)
    if len(indexes) < 1:
        os.system('cls')
        print(response)
        print("Try again!")
        
        return response
    for i in range(len(response)):
        if i in indexes:
            new_response[i] = rat
        else:
            continue
    response = ""
    for i in new_response:
        response += i
    print(response)
    return response


def start_game():
    wort = getwort()
    dic = arbeit(wort)
    response = ""
    for i in range(len(wort)):
        response += "_"
    print(response)

    print("raten...",end="")
    while "_" in response:
        rat = input("\n")
        rat = rat.upper()
        response = check(rat, dic, response)




    


def run():
    start_game()


if __name__ == '__main__':
    run()