def run():
    import sqlite3

    conn = sqlite3.connect('pokedex.sqlite')
    cur = conn.cursor()
    integer = False
    corrected = False

    my_team = list()
    opposite_team = list() 

    #Filling up my team
    for add in range(6):
        while True:
            pokemon = input('What Pokemon would you like to choose? (insert Pokemon''s name or id!)\n')
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
                cur.execute('''SELECT ab_id, game_id, chain_id FROM Members WHERE poke_id = ?''',(pkid,))
                for i in cur:
                    pkab = i[0]
                    apid = i[1]
                    chid = i[2]
                print(pkid, pkab, apid, chid)
        cur.execute('''SELECT Pokemon.name, Pokemon.type, Abilities.name, Abilities.effect, 
        Games.games, Abilities.pokeshare, Abilities.de_name, Evochain.evolves_to
        FROM Pokemon JOIN Abilities JOIN Games JOIN Evochain ON
        Pokemon.id = ? AND
        Abilities.id = ? AND
        Games.pokemon_id = ?''', (pkid, pkab, apid))
        for i in cur:
            pname = i[0]
            ptypes = i[1]
            abname = i[2]
            peffect = i[3]
            pgames = i[4]
            pwith = i[5]
            pab = i[6]
            evo = i[7]

        evolves_to = ""
        evos = evo.split(", ")
        if evos[0] == "": evolves_to += "None"
        elif pkid == int(evos[1].split(":")[1]): evolves_to += evos[0].split(":")[0]
        elif pkid == int(evos[0].split(":")[1]): evolves_to += "None"
        else: evolves_to += evos[1].split(":")[0]

        pokemon_to_add = dict()
        poke_with_ids = pwith.split()
        gamesin = pgames.split()
        poke_with = list()
        ptype = ptypes.split(", ")

        print(poke_with_ids)
        for id in poke_with_ids:
            cur.execute('SELECT name FROM Pokemon WHERE id = ?', (id,))
            poke_with.append(cur.fetchone()[0])
        weak_tos = list()
        weak_fors = list()
        strong_tos = list()
        strong_fors = list()
        no_damage_tos = list()
        no_damage_fors = list()

        for t in ptype:
            cur.execute('''SELECT weak_to, weak_for, strong_to, strong_for, no_damage_to, no_damage_for FROM Types where name = (?)''', (t,))
            for i in cur:
                weak_to = i[0]
                weak_for = i[1]
                strong_to = i[2]
                strong_for = i[3]
                no_damage_to = i[4]
                no_damage_for = i[5]

                weak_tos.append(weak_to)
                weak_fors.append(weak_for)
                strong_tos.append(strong_to)
                strong_fors.append(strong_for)
                if not no_damage_to == "none":
                    no_damage_tos.append(no_damage_to)
                if not no_damage_for == "none":
                    no_damage_fors.append(no_damage_for)


        pokemon_to_add['name'] = pname
        pokemon_to_add['type'] = ptype
        pokemon_to_add['ability'] = pkab
        pokemon_to_add['effect'] = peffect
        pokemon_to_add['games'] = pgames
        pokemon_to_add['evolves_to'] = evolves_to
        pokemon_to_add['pokeshare'] = poke_with
        pokemon_to_add['weak_to'] = weak_tos
        pokemon_to_add['weak_for'] = weak_fors
        pokemon_to_add['strong_to'] = strong_tos
        pokemon_to_add['strong_for'] = strong_fors
        pokemon_to_add['no_damage_to'] = no_damage_tos
        pokemon_to_add['no_damage_for'] = no_damage_fors

        my_team.append(pokemon_to_add)

      
            
        

            
             


    


if __name__ == '__main__':
    run()