def run():
    import sqlite3

    conn = sqlite3.connect('pokedex.sqlite')
    cur = conn.cursor()
    integer = False
    corrected = False
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
        cur.execute('''SELECT id FROM Pokemon WHERE APId = (?)''',(pokemon,))
    else:
        cur.execute('''SELECT id FROM Pokemon WHERE name = (?)''',(pokemon,))
    
    try:
        pkid = cur.fetchone()[0]
        cur.execute('''SELECT ab_id, game_id FROM Members WHERE poke_id = ?''',(pkid,))
        for i in cur:
            pkab = i[0]
            apid = i[1]
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
                    corrected = True
                    break  
        except IndexError:
            print("this pokemon is not in our pokedex!\n")
            quit()
        except Exception as err:
            print(err)
            quit()
        
        if corrected:
            cur.execute('''SELECT id FROM Pokemon WHERE name = (?)''', (pokemon,))
            pkid = cur.fetchone()[0]
            cur.execute('''SELECT ab_id, game_id FROM Members WHERE poke_id = ?''',(pkid,))
            for i in cur:
                pkab = i[0]
                apid = i[1]
            print(pkid, pkab, apid)
    cur.execute('''SELECT Pokemon.name, Abilities.name, Abilities.effect, Games.games, Abilities.pokeshare
    FROM Pokemon JOIN Abilities JOIN Games ON
    Pokemon.id = ? AND
    Abilities.id = ? AND
    Games.pokemon_id = ?''', (pkid, pkab, apid))
    for i in cur:
        pname = i[0]
        abname = i[1]
        peffect = i[2]
        pgames = i[3]
        pwith = i[4]
    poke_with_ids = pwith.split()
    gamesin = pgames.split()
    poke_with = list()
    
    print(poke_with_ids)
    for id in poke_with_ids:
        cur.execute('SELECT name FROM Pokemon WHERE id = ?', (id,))
        poke_with.append(cur.fetchone()[0])
    print("Your pokemon is: "+ pname +", with pokedex number:"+str(apid)+ ", that shares ability with the following pokemons: ", end="")
    c = 0 
    for p in poke_with:
        if c > 0:
            print(", "+p,end="")
        else:
            print(p, end=" ")
        c += 1
    print("\nand appears in the following games: ")
    c = 0
    for g in gamesin:
        if c > 0:
            print(", "+g, end="")
        else:
            print(g, end="")
        c += 1

    print("\nIts ability is: "+abname+", and has the following effect:")
    print(peffect)        
            
        

            
             


    


if __name__ == '__main__':
    run()