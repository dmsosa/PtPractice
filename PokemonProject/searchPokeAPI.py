def run():
    import sqlite3

    conn = sqlite3.connect('pokedex.sqlite')
    cur = conn.cursor()
    integer = False
    while True:
        pokemon = input('What Pokemon would you like to find? (insert Pokemon''s name or id!)\n')
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
        for i in cur:
            pkid = i[0]
            pkname = i[1]
            pkab = i[2]
        print(cur.fetchone(), pkid, pkname, pkab, "yo")

        cur.execute('''SELECT Pokemon.id, Pokemon.name, Pokemon.ability, Abilities.effect, 
        Abilities.pokeshare, Games.games, Games.gen FROM Pokemon JOIN Abilities JOIN Games ON 
        Abilities.name = (?) AND Games.pokemon_id = (?)''',(pkab, pkid))

    except UnboundLocalError:
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
                elif typo.lower() == "yes":
                    pokemon = sorted_suggestion[0][1]
                    break  
        except IndexError:
            print("this pokemon is not in our pokedex!\n")
            quit()
        except Exception as err:
            print(err)
            quit()
        
    cur.execute('''SELECT id, name, ability, APId FROM Pokemon WHERE name = (?)''', (pokemon,))

    for i in cur:
        pkid = i[0]
        pkname = i[1]
        pkab = i[2]
        apid = i[3]
    print(cur.fetchone(), pkid, pkname, pkab, "ya")

    cur.execute('''SELECT Abilities.effect, Games.games
    FROM Abilities JOIN Games ON 
    Abilities.name = (?)
    AND Games.pokemon_id = (?)''',(pkab, apid))
    print(cur.fetchone())

        

            
             


    


if __name__ == '__main__':
    run()