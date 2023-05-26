def run():
    import sqlite3
    import numpy as np
    import random
    import math

    conn = sqlite3.connect('pokedex.sqlite')
    cur = conn.cursor()
    integer = False
    corrected = False

    my_team = list()
    opposite_team = list() 
    times = 6
    #Filling up my team
    while times > 0:
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
            cur.execute('''SELECT ab_id, game_id, chain_id FROM Members WHERE poke_id = ?''',(pkid,))
            for i in cur:
                pkab = i[0]
                apid = i[1]
                chid = i[2]
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
                continue
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
        Games.games, Abilities.pokeshare, Abilities.de_name, Evochain.first, Evochain.evolves_to
        FROM Pokemon JOIN Abilities JOIN Games JOIN Evochain ON
        Pokemon.id = ? AND
        Abilities.id = ? AND
        Games.pokemon_id = ? AND
        Evochain.chid = ?''', (pkid, pkab, apid, chid))
        for i in cur:
            pname = i[0]
            ptypes = i[1]
            abname = i[2]
            peffect = i[3]
            pgames = i[4]
            pwith = i[5]
            pab = i[6]
            first = i[7]
            evo = i[8]

        for p in my_team:
            if p['name'] == pname:
                print("This pokemon is already in your team!")
                pname = 'Found'
                continue
        if pname == 'Found':
            continue

        evolves_to = ""
        evos = evo.split(", ")
        if evos[0] == "": evolves_to += "None"
        elif len(evos) > 1:
            if pkid == first: evolves_to += evos[1].split(":")[0]
            elif pkid == int(evos[0].split(":")[1]): evolves_to += "None"
            elif pkid == int(evos[1].split(":")[1]): evolves_to += evos[0].split(":")[0]
        else:
            if pkid == first: evolves_to += evos[0].split(":")[0]
            else: evolves_to += 'None'

        pokemon_to_add = dict()
        poke_with_ids = pwith.split()
        gamesin = pgames.split()
        poke_with = list()
        ptype = ptypes.split(", ")
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
        print("Mein pokemon\n")
        print(pokemon_to_add)
        times -= 1

        cur.execute("SELECT * FROM Members ORDER BY RANDOM() LIMIT 1")
        for j in cur:
            opid = j[0]
            opab = j[1]
            opga = j[2]
            opev = j[3]
        cur.execute('''SELECT Pokemon.name, Pokemon.type, Abilities.name, Abilities.effect, 
        Games.games, Abilities.pokeshare, Abilities.de_name, Evochain.first, Evochain.evolves_to
        FROM Pokemon JOIN Abilities JOIN Games JOIN Evochain ON
        Pokemon.id = ? AND
        Abilities.id = ? AND
        Games.pokemon_id = ? AND
        Evochain.chid = ?''', (opid, opab, opga, opev))
        for j in cur:
            opname = j[0]
            optype = j[1]
            opabil = j[2]
            opeffect = j[3]
            opgames = j[4]
            opshare = j[5]
            opdename = j[6]
            opfirst = j[7]
            opevos = j[8]

        evolves_to = ""
        evos = opevos.split(", ")
        if evos[0] == "": evolves_to += "None"
        elif len(evos) > 1:
            if opid == opfirst: evolves_to += evos[1].split(":")[0]
            elif opid == int(evos[0].split(":")[1]): evolves_to += "None"
            elif opid == int(evos[1].split(":")[1]): evolves_to += evos[0].split(":")[0]
        else:
            if opid == opfirst: evolves_to += evos[0].split(":")[0]
            else: evolves_to += 'None'
        
        opposite_poke = dict()
        opwith_id = opshare.split()
        opwith = list()
        opgamesin = opgames.split()
        optypes = optype.split(", ")
        for id in opwith_id:
            cur.execute('SELECT name FROM Pokemon WHERE id = ?',(id,))
            opwith.append(cur.fetchone()[0])

        opweak_tos = list()
        opweak_fors = list()
        opstrong_tos = list()
        opstrong_fors = list()
        opno_damage_tos = list()
        opno_damage_fors = list()


        for t in optype.split():
            cur.execute('''SELECT weak_to, weak_for, strong_to, strong_for, no_damage_to, no_damage_for FROM Types where name = (?)''', (t,))
            for j in cur:
                weak_to = i[0]
                weak_for = i[1]
                strong_to = i[2]
                strong_for = i[3]
                no_damage_to = i[4]
                no_damage_for = i[5]
            opweak_tos.append(weak_to)
            opweak_fors.append(weak_for)
            opstrong_tos.append(strong_to)
            opstrong_fors.append(strong_for)
            if no_damage_to != "none":
                opno_damage_tos.append(no_damage_to)
            if no_damage_to != "none":
                opno_damage_fors.append(no_damage_for)

        opposite_poke['name'] = opname
        opposite_poke['type'] = optypes
        opposite_poke['ability'] = opabil
        opposite_poke['effect'] = opeffect
        opposite_poke['games'] = opgamesin
        opposite_poke['evolves_to'] = evolves_to
        opposite_poke['pokeshare'] = opwith
        opposite_poke['weak_to'] = weak_tos
        opposite_poke['weak_for'] = weak_fors
        opposite_poke['strong_to'] = strong_tos
        opposite_poke['strong_for'] = strong_fors
        opposite_poke['no_damage_to'] = no_damage_tos
        opposite_poke['no_damage_for'] = no_damage_fors

        opposite_team.append(opposite_poke)

    print("Die Pokemonkampf beginn kann!")
    vector_type = np.array([1, 1.5, -1.5, -1, -2, 2])
    score = {"myteam":0, "opteam":0}
    for i in range(6):
        my_values = [0, 0, 0, 0, 0 , 0]
        op_values = [0, 0, 0, 0, 0 , 0]
        print(my_team[i]['name']+ " gegen: "+ opposite_team[i]['name'])
        for j in my_team[i]['type']:
            for t in opposite_team[i]['weak_to']:
                if j in t:my_values[0] += 1
            for t in opposite_team[i]['weak_for']:
                if j in t:my_values[1] += 1
            for t in opposite_team[i]['strong_to']:
                if j in t:my_values[2] += 1
            for t in opposite_team[i]['strong_for']:
                if j in t:my_values[3] += 1
            for t in opposite_team[i]['no_damage_to']:
                if j in t:my_values[4] += 1
            for t in opposite_team[i]['no_damage_for']:
                if j in t:my_values[5] += 1

        for j in opposite_team[i]['type']:
            for t in my_team[i]['weak_to']:
                if j in t:op_values[0] += 1
            for t in my_team[i]['weak_for']:
                if j in t:op_values[1] += 1
            for t in my_team[i]['strong_to']:
                if j in t:op_values[2] += 1
            for t in my_team[i]['strong_for']:
                if j in t:op_values[3] += 1
            for t in my_team[i]['no_damage_to']:
                if j in t:op_values[4] += 1
            for t in my_team[i]['no_damage_for']:
                if j in t:op_values[5] += 1
        m = np.array([my_values, op_values])
        print(m)
        result = np.dot(m, vector_type)
        print(result)
        if result[0] > result[1]: 
            print(my_team[i]['name'] + " wins this battle!") 
            score['myteam'] += 1
        elif result[1] > result[0]: 
            print(my_team[i]['name'] + " kann nicht mehr weiter kampfen, "+opposite_team[i]['name']+" hab gewonnen!")
            score['opteam'] += 1
        else: 
            rand = math.floor(random.random()*2)
            if rand == 0:
                print(my_team[i]['name'] + " wins this battle!") 
                score['myteam'] += 1
            else:
                print(my_team[i]['name'] + " kann nicht mehr weiter kampfen, "+opposite_team[i]['name']+" hab gewonnen!")
                score['opteam'] += 1

    print(score)
    if score['myteam'] > score['opteam']: 
        print("wir haben gewonnen!")
    elif score['opteam'] > score['myteam']: 
        print("wir haben verloren!")
    else: print("draw!")
             


    


if __name__ == '__main__':
    run()