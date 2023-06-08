import math, random, os, time
def try_again(game):
    new_game = False
    if game:
        print("Du schafftet es!\nMochtest du noch einmal spielen?")
    else:
        print("Game over!\nMochtest du es noch einmal versuchen?")
    while True:
        ans = input(">")
        if ans.lower() == 'yes':
            new_game = True
            print('Das ist es!\nLos gehts!')
            time.sleep(2)
            os.system('cls')
            return new_game
        elif ans.lower() == 'no':
            print('Wir hoffen es, du noch einmail wiedersehen!')
            time.sleep(2)
            print('Tschuss!')
            return new_game

def fill(todraw, indexes):
    new_response = list()
    rat = list(indexes.keys())[0]
    index = list(indexes.values())[0]
    for i in todraw['response']:
        new_response.append(i)
    for i in range(len(new_response)):
        if i in index:
            new_response[i] = rat
    todraw['response'] = ""
    for i in range(len(new_response)):
        todraw['response'] += new_response[i]
    os.system('cls')
    print(todraw['bars']+"\n "+todraw['response']+"\n"+todraw['bars'])
    print(todraw['man'])
    return todraw

    
def draw(scores, todraw):
    os.system('cls')
    print(todraw['bars']+"\n "+todraw['response']+"\n"+todraw['bars'])
    model_3 = "  ____\n |    |\n |    O\n |   /|\\\n |   / \\\n | \n_|_\n"
    todraw['man'] = model_3[:(scores['fails']*4)+1]
    for i in range(scores['fails']*4):
        print(model_3[i], end="")
    print("")
    return todraw

   
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
    game = True
    random_messages = {'positive':['Gut gemacht!', 'Du bist toll!','Eine gute Vermutung', 'Der war gut!']}
    while game:
        os.system('cls')
        wort = getwort()
        dic = arbeit(wort)
        scores = {'fails':0, 'guts':0, 'double':0, 'row':0, 'guesses':[], 'maxrow':0, 'points':0}
        todraw = {'response':"",'bars':"//", 'man':""}
        for i in range(len(wort)):
            todraw['bars'] += "/"
            todraw['response'] += "_"
        print(todraw['bars']+"\n "+todraw['response']+"\n"+todraw['bars'])

        print("raten...",end="")
        while "_" in todraw['response']:
            rat = input("\n")
            rat = rat.upper()
            if len(rat) != 1:
                print("invalid raten!")
                continue
            if rat not in scores['guesses'] : scores['guesses'].append(rat)
            else: 
                print('You already tried with that one!')
                continue
            indexes = check(rat, dic)
            if len(indexes) > 0:
                scores['guts'] += 1
                scores['row'] += 1
                if scores['row'] > scores['maxrow']:
                    scores['maxrow'] = scores['row']
                if scores['row'] > 2:
                    print(str(scores['row'])+" guesses in a row! +20")
                    scores['double'] += 1
                    scores['points'] += 20
                else:
                    scores['points'] += 10
                todraw = fill(todraw, indexes)
            else:
                print('Not found!\n-10 points')
                scores['points'] -= 10
                scores['fails'] += 1
                if scores['row'] > 2:
                    print("Oh, you lost it...")
                scores['row'] = 0
                todraw = draw(scores, todraw)
                if scores['fails'] == 12:
                    print('//////////////////////\nRuhe in Frieden x_x')
                    break
        if scores['fails'] == 0:
            print("OMG! Zapatero!")
        if scores['fails'] == 12:
            game = False
            game = try_again(game)
        else:
            game = True
            game = try_again(game)
        return scores
def showscore(prepared_rows):
    todraw = {'roof':"==========o=========="}
    print(todraw['roof'])
    for i in prepared_rows.values():
        print("|"+i)
    print(todraw['roof'])
def prepare_row(scores):
    table_rows = {}
    for stat, n in scores.items():
        if stat == 'guesses':
            n = len(n)
        row = str(stat)+":"+str(n)+"|"
        pos = row.find(":")
        space = row[pos:pos+1]
        while len(space)+len(row) < 20:
            space += " "
        row = str(stat)+space+str(n)+"|"
        table_rows[stat] = row
    return table_rows
    

    


def run():
    scores = start_game()
    table_rows = prepare_row(scores)
    showscore(table_rows)
    

if __name__ == '__main__':
    run()