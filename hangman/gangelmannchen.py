import math, random, os, time
def fill(response, indexes, man):
    new_response = list()
    rat = list(indexes.keys())[0]
    index = list(indexes.values())[0]
    bars = "- "
    for i in response:
        new_response.append(i)
    for i in range(len(response)):
        bars += "-"
        if i in index:
            new_response[i] = rat
    response = ""
    for i in range(len(new_response)):
        response += new_response[i]
    os.system('cls')
    print("   "+response+"\n"+bars+" -")
    print(man)
    print('Gut gemacht!')
    return response

    
def draw(response, man, fails):
    os.system('cls')
    print("   "+response+"\n")
    model_3 = "  ____\n |    |\n |    O\n |   /|\\\n |   / \\\n | \n_|_\n"
    man = model_3[0:(fails*4+1)]
    for i in range(fails*4):
        print(model_3[i], end="")
    print("")
    return man
   
def getwort():
    with open("./data.txt", "r") as f:
        worter = f.read().split("\n")
        rand = math.floor(random.random()*(len(worter)))
        wort = worter[rand].upper()
        return wort

def arbeit(wort):
    dic = {k:[i for i in range(len(wort)) if wort[i] == k] for k in wort}
    return dic

def check(rat, dic):

    indexes = {}
    if rat in dic.keys():
        indexes[rat] = dic.get(rat)
    return indexes


def start_game():
    os.system('cls')
    
    gover = False
    gwon = False
    try_again = False
    wort = getwort()
    dic = arbeit(wort)
    response = ""
    man = ""
    fails = 0
    guesses = list()
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
            response = fill(response, indexes, man)
        else:
            print('Not found!')
            fails += 1
            man = draw(response, man, fails)
            if fails == 12:
                print('//////////////////////\nRuhe in Frieden x_x')
                break
    if gover:
        while True:
            ans = input(" . . . (game over) . . .\nwant to try again?")
            if ans.lower() == 'yes':
                try_again = True
                print('Das ist es!\nLos gehts!')
                time.sleep(2)
                os.system('cls')
                break
            elif ans.lower() == 'no':
                print('Wir hoffen es, du noch einmail wiedersehen!')
                time.sleep(2)
                print('Tschuss!')
                break
    elif gwon:
        while True:
            ans = input("Du schafftet es!\nMochtest du noch einmal spielen?")
            while True:
                ans = input(" . . . (game over) . . .\nwant to try again?")
                if ans.lower() == 'yes':
                    try_again = True
                    print('Das ist es!\nLos gehts!')
                    time.sleep(2)
                    os.system('cls')
                    break
                elif ans.lower() == 'no':
                    print('Wir hoffen es, du noch einmail wiedersehen!')
                    time.sleep(2)
                    print('Tschuss!')
                    break
    return try_again




    


def run():
    spiel = start_game()
    while spiel:
        spiel = start_game()


if __name__ == '__main__':
    run()