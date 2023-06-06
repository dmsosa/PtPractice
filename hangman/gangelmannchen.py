import math, random, os
def fill(response, indexes, man):
    new_response = list()
    rat = list(indexes.keys())[0]
    index = list(indexes.values())[0]

    for i in response:
        new_response.append(i)
    for i in range(len(response)):
        if i in index:
            new_response[i] = rat
    response = ""
    for i in range(len(new_response)):
        response += new_response[i]
    os.system('cls')
    print(response)
    print(man)
    print('Gut gemacht!')

    
def draw(response, man, fails):
    print(response)
    if fails == 1:
        man += ""
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

def check(rat, dic):

    indexes = {}
    if rat in dic.keys():
        indexes[rat] = dic.get(rat)
        return indexes
    elif len(indexes) < 1:
        return indexes


def start_game():
    os.system('cls')
    
    wort = getwort()
    dic = arbeit(wort)
    response = ""
    fails = 0
    guesses = list()
    man = ""
    for i in range(len(wort)):
        response += "_"
    print(response)

    print("raten...",end="")
    while "_" in response:
        rat = input("\n")
        rat = rat.upper()
        if len(rat) != 1:
            print("invalid raten!")
            continue
        if rat not in guesses : guesses.append(rat)
        else: 
            print('You already tried with that one!')
            continue
        indexes = check(rat, dic)
        if len(indexes) > 0:
            fill(response, indexes, man)
        else:
            print('Not found!')
            fails += 1
            draw(response, man, fails)
            continue




    


def run():
    dif = 48
    man = ""
    while dif > 0:
        p1 = "  ____\n"
        p2 = " |    |\n"
        p3 = " |    O\n"
        p4 = " |   /|\\\n"
        p5 = " |   / \\\n"
        p6 = " | \n"
        p7 = "_|_\n"
        total = p1+p2+p3+p4+p5+p6+p7
        model_1 = "      \n | \n | \n | \n | \n | \n_|_\n"
        model_2 = " ____\n |    |\n | \n | \n | \n | \n_|_\n"
        model_3 = " ____\n |    |\n |    O\n |   /|\\\n |   / \\\n | \n_|_\n"
        print(len(" |   / \\\n"))
        print(model_1, model_2, model_3)
        f = int(input('from'))
        t = int(input('to'))
        print(total[f:t])
        # print(str(len(total))+"\n"+total)
        # dif = len(total) - len(man) - 4
        # steps = 48 - dif
        # step = int(steps/4)

        # man = ""
        # for i in range(step):
        #     if 0 <= i <= 2:
        #         man += total[i]
        #     man += total[i]

        # if steps == 48:
        #     print("Ruhe in Frieden x_x")
        # print(man)
        # e = input("step "+ str(int(steps/4))+" out of 12")


if __name__ == '__main__':
    run()