def run():
    import sqlite3

    conn = sqlite3.connect('pokedex.sqlite')
    cur = conn.cursor()
    integer = False
    while True:
        pokemon = input('What Pokemon would you like to find? (insert Pokemon''s name or id!)\n')
        if len(pokemon) < 1:
            continue
        try: 
            pokemon = int(pokemon)
            integer = True
            break
        except:
            pokemon = pokemon.lower()
            if len(pokemon) < 3:
                continue
            break

    if integer:
        print("i")
        cur.execute('''SELECT id, name, ability FROM Pokemon WHERE APId = (?)''',(pokemon,))
    else:
        cur.execute('''SELECT id, name, ability FROM Pokemon WHERE name = (?)''',(pokemon,))

    try: 
        poke = cur.fetchone()[0]
    except TypeError:
        try:
            suggestions = dict()
            sorted_suggestion = list()
            cur.execute("SELECT name FROM Pokemon")
            for poke in cur:
                name = poke[0]
                commonLetter = 0
                if len(name) < len(pokemon):
                    continue
                if not (pokemon[:3] in name):
                    continue
                # if not name.startswith(pokemon[:3]):
                #     continue
                for letter in range(len(name)):
                    try:
                        if name[letter+name.index(pokemon[:3])] == pokemon[letter]:
                            commonLetter += 1
                    except IndexError:
                        break
                suggestions[name] = commonLetter

            for k,v in suggestions.items():
                sorted_suggestion.append((v,k))
            sorted_suggestion = sorted(sorted_suggestion, reverse=True)
            while True:
                typo = input("perhaps you wanted to type: '"+sorted_suggestion[0][1]+"'?\n")
                if len(typo) < 1 or typo.lower() == "no":
                    print("this pokemon is not in our pokedex!\n")
                    return
                if typo.lower() == "yes":
                    pokemon = sorted_suggestion[0][1]
        except IndexError:
            print("this pokemon is not in our pokedex!\n")
            quit()
        except Exception as err:
            print(err)
            quit()
    if cur.fetchone() is None:
        cur.execute('''SELECT id, name, ability FROM Pokemon WHERE name = (?)''', (pokemon,))
    pkid = cur.fetchone()[0]
    pkname = cur.fetchone()[1]
    pkab = cur.fetchone()[2]
    cur.execute('''SELECT Pokemon.id, Pokemon.name, Pokemon.ability, Abilities.effect, 
    Abilities.pokeshare, Games.games, Games.gen FROM Pokemon JOIN Abilities JOIN Games ON 
    Abilities.name = (?) AND Games.pokemon_id = (?)''',(pkab, pkid))

        

            
             


    


if __name__ == '__main__':
    run()