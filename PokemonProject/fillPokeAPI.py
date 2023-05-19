#This program fills up our database with pokemon! (some of them I did not even know that existed!)

def run():
    import urllib.request, urllib.parse, urllib.error
    import math, random #math and random are just imported to pick an ability for our Pokemon randomly
    import sqlite3
    import requests
    import json
    

    def fillPokemon():
        conn = sqlite3.connect('pokedex.sqlite')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Pokemon (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        ability TEXT NOT NULL,
        hidden INTEGER,
        APId INTEGER
        )''')

        #Checking if the table is already filled with data

        cur.execute('SELECT * FROM Pokemon')
        if len(cur.fetchall()) > 1:
            print("Table already filled up!")
            return
        
        #//////////////////////////////////////////////////////////
        serviceurl = "https://pokeapi.co/api/v2/pokemon/{name}/"
        while True:
            pokemon = input('ready to fill up our database?')
            if len(pokemon) < 1 or pokemon.lower() == "yes":
                break

        try:
            for n in range(1, 1000):
                pkmn = requests.get(serviceurl.format(name=n))
                pkdata = json.loads(pkmn.text)
                suggestName = pkdata['name']
                APid = pkdata['id']
                type = ""
                ability = ""
                hidden = None
                for types in pkdata['types']:
                    if len(type) > 1:
                        type += ", "
                    type += types['type']['name']
                for ability in pkdata['abilities']:
                    x = math.floor(random.random()*len(pkdata['abilities']))
                    ability = pkdata['abilities'][x]['ability']['name']
                    if not pkdata['abilities'][x]['is_hidden']:
                        hidden = 0
                    else:
                        hidden = 1
                
                try:
                    cur.execute('''INSERT OR IGNORE INTO Pokemon (name, type, ability, hidden, APId)
                    VALUES (?,?,?,?,?)''', (suggestName, type, ability, hidden, APid))
                    print("New pokemon registered!")
                except:
                    print("Something went wrong!")
            conn.commit()
            conn.close()     
        except:
            pass
    
    def fillEvos():


        conn = sqlite3.connect('pokedex.sqlite')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Evochain (
        chid INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
        first INTEGER,
        evolves_to TEXT
        )''')
        
        #Checking if the table is already filled with data
        cur.execute('SELECT * FROM Evochain')
        if len(cur.fetchall()) > 1:
            print("Table already filled up!")
            return
        
        #//////////////////////////////////////////////////////////
        for n in range (1, 1000):
            try:
                f = requests.get(f'https://pokeapi.co/api/v2/evolution-chain/{n}/')
                js = json.loads(f.text)
                chain_id = js['id']
                first = js['chain']['species']['name']
                evolutions = dict()
                for evo in js['chain']['evolves_to']:
                    try:
                        thi = evo['evolves_to'][0]
                        thi_name = evo['evolves_to'][0]['species']['name']
                        evolutions[thi_name] = None
                        try:
                            fourth = thi['evolves_to'][0]['species']['name']
                        except:
                            pass
                    except:
                        pass
                    sec = evo['species']['name']
                    evolutions[sec] = None
                


                cur.execute('''SELECT id FROM Pokemon WHERE name = ?''', (first,))
                first_id = cur.fetchone()[0]

                for poke in evolutions.keys():
                    cur.execute('''SELECT id FROM Pokemon WHERE name = ?''', (poke,))
                    evolutions[poke] = cur.fetchone()[0]
                
                evos = ""
                for poke, id in evolutions.items():
                    evos += poke+":"+str(id)
                    if len(poke) > 1:
                        evos += ", "
                evos = evos[:-2]
                print(evos)
                cur.execute('INSERT OR IGNORE INTO Evochain (chid, first, evolves_to) VALUES (?, ?, ?)',( first_id, evos))
            except Exception as err:
                print(err)
                continue
        conn.commit()
        cur.close()




    def fillAbs():


        serviceurl = 'https://pokeapi.co/api/v2/ability/{}'
        conn = sqlite3.connect('pokedex.sqlite')
        cur = conn.cursor()

        #Checking if the table is already filled with data
        cur.execute('SELECT * FROM Abilities')
        if len(cur.fetchall()) > 1:
            print("Table already filled up!")
            return
            
        cur.execute('''CREATE TABLE IF NOT EXISTS Abilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        effect TEXT,
        de_name TEXT NOT NULL UNIQUE,
        pokemon_with INTEGER,
        pokemon_hidden INTEGER,
        pokeshare TEXT
        );''')

        while True:
            auto = False
            many = input("How many abilities do you want to look for?\n")
            try: 
                many = int(many)
            except:
                continue
            if many == 0:
                print("You think you are funny, right?\n")
                quit()
            elif many > 10:
                auto = True
                automatic = input("those are a few, do you want to fill up automaticly?")
                while automatic.lower() != "no" and automatic.lower() != "yes":
                    automatic = input("Excuse me, do you want to fill up the data automaticly?")
                    if automatic.lower() == "yes":
                        auto = True
                        break
                    else:
                        break
                break
            else:
                break
 
                

        while many > 0:
            if auto:
                cur.execute('SELECT ability FROM Pokemon ORDER BY RANDOM() LIMIT 1')
                ab = cur.fetchone()[0]
            else:
                answer = ""
                ab = input("Insert ability name, bitte!\n")
                many -= 1
                try:
                    uh = requests.get(serviceurl.format(ab))
                    if uh.text.lower() == 'not found' or (len(ab) < 1) or (uh.text is None) < 0:
                        while True:
                            answer = input("That ability was not found, do you want to search one randomly?\n")
                            if len(answer) < 1 or answer.lower() == 'no':
                                print("Okay!")
                                break
                            if answer.lower() == 'yes':
                                break
                    
                except Exception as err:
                    print(err)
                    continue
                
                if answer == "yes":
                    cur.execute('SELECT ability FROM Pokemon ORDER BY RANDOM() LIMIT 1')
                    ab = cur.fetchone()[0]
                    cur.execute('SELECT name FROM Abilities WHERE name = (?)',(ab,))
                    try:
                        if len(cur.fetchone()[0]) > 1:
                            print("That ability was already retrieved")
                            many -= 1
                            continue
                    except TypeError:
                        pass

            try:
                uh = requests.get(serviceurl.format(ab))
                many -= 1
                js = json.loads(uh.text)
            except Exception as err:
                print(err)
                many -= 1
                continue

            try:
                de_effect = ''
                for name in js['names']:
                    if name['language']['name'] == "de":
                        de_name = name['name']
                for effect in js['effect_entries']:
                    if effect['language']['name'] == "de":
                        de_effect = effect['effect']

                poke_with = dict()
                for poke in js['pokemon']:
                    if not poke['is_hidden']:
                        hid = 0
                    else:
                        hid = 1
                    poke_name = poke['pokemon']['name']
                    poke_with[poke_name] = hid

                poke_hid = 0
                poke_no_hid = 0
                poke_with_ids = list()

                for k,v in poke_with.items():
                    if v == 1:
                        poke_hid += 1
                    else: 
                        poke_no_hid += 1


                    cur.execute('SELECT id FROM Pokemon WHERE name = (?)',(k,))
                    try:
                        pokeid = cur.fetchone()[0]
                        poke_with_ids.append(pokeid)
                    except:
                        continue

                pokeshare_id = ""
                c = 0
                for id in poke_with_ids:
                    if c > 1:
                        pokeshare_id += " "+str(id)
                    else:
                        pokeshare_id += str(id)
                    c += 1
                cur.execute('''INSERT OR IGNORE INTO Abilities (name, effect, de_name, pokemon_with, pokemon_hidden, pokeshare)
                VALUES (?, ?, ?, ?, ?, ?)''', (ab, de_effect, de_name, poke_no_hid, poke_hid, pokeshare_id))
                print("new ability added to our pokedex")
            except KeyError:
                pass
            


        conn.commit()
        cur.close()
        return

    def fillGames():
        conn = sqlite3.connect('pokedex.sqlite')
        cur = conn.cursor()

        #Checking if the table is already filled with data
        cur.execute('SELECT * FROM Games')
        if len(cur.fetchall()) > 1:
            print("Table already filled up!")
            return
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Games (
        pokemon_id INTEGER NOT NULL UNIQUE,
        games TEXT,
        gen TEXT NOT NULL
        )''')

        while True:
            how_many = input("Start the filling!\n")
            
            try:
                how_many = int(how_many)
                if how_many == 0:
                    print("0 times! are you serious?")
                    continue
                break
            except:
                continue

        while how_many > 0:
            cur.execute('''SELECT APId FROM Pokemon ORDER BY RANDOM() LIMIT 1''')
            id = cur.fetchone()[0]
            url = "https://pokeapi.co/api/v2/pokemon/{poke}/"
            uh = requests.get(url.format(poke=id))
            try:
                js = json.loads(uh.text)
            except Exception as err:
                print(err)
                how_many -= 1
                continue

            game_names = list()
            games = ""  
            for index in js['game_indices']:
                gname = index['version']['name']
                game_names.append(gname)
            
            c = 0
            for g in game_names:
                if c > 0:
                    games += " "+g
                c += 1
            url = "https://pokeapi.co/api/v2/pokemon-species/{poke}/"
            uh = requests.get(url.format(poke=id))
            try:
                js = json.loads(uh.text)
            except Exception as err:
                print(err)
                how_many -= 1
                continue
            gen = js['generation']['name']

            cur.execute('''INSERT OR IGNORE INTO Games (pokemon_id, games, gen) VALUES(?, ?, ?)''', (id, games, gen))
            print("new pokemon added!")
            how_many -= 1
        conn.commit()
        cur.close()

    def relate():
        conn = sqlite3.connect('pokedex.sqlite')
        cur = conn.cursor()
        cur.executescript('''CREATE TABLE IF NOT EXISTS Members (
        poke_id INTEGER,
        ab_id INTEGER,
        game_id INTEGER,
        PRIMARY KEY (poke_id, ab_id, game_id)
        )''')


        cur.execute('SELECT id FROM Pokemon')
        pkty = len(cur.fetchall())
        cur.execute('SELECT poke_id FROM Members')
        abidqty = len(cur.fetchall())
        if (pkty - abidqty) < 100:
            print("Our data was already related up!")
            return
        
        to_find = input("press to relate!\n")
        if to_find.lower() == "exit":
            return

        try:
            cur.execute('SELECT id, ability, APId FROM Pokemon')
            for i in cur.fetchall():
                pkid = i[0]
                pkab = i[1]
                apid = i[2]
                try:
                    cur.execute('SELECT * FROM Members WHERE poke_id = ? AND ab_id = ? AND game_id = ?',(pkid, abid, apid))
                    if len(cur.fetchone()) > 1:
                        print("That Poke was already related!")
                except:
                    try:
                        cur.execute('SELECT id FROM Abilities WHERE name = (?)', (pkab,))
                        abid = cur.fetchone()[0]
                    except:
                        print("That ab was not found!")
                        continue
                    cur.execute('INSERT OR IGNORE INTO Members (poke_id, ab_id, game_id) VALUES (?, ?, ?)', (pkid, abid, apid))
                    print("Succesfully added!")
                    print(pkid, pkab, apid)
        except Exception as err:
            print(err)
            print("That Pokemon is not in our pokedex!")


            #checking if the data is not already inserted
            
        
        conn.commit()
        cur.close()

    while True:
        todo = input("Which Data do you want to fill up?\n")
        if len(todo) < 1:
            relate()
            continue
        if todo.lower() == "pokemon":
            fillPokemon()
            break
        elif todo.lower() == "evos":
            fillEvos()
            break
        elif todo.lower() == "abs":
            fillAbs()
            break
        elif todo.lower() == "games":
            fillGames()
            break
        elif todo.lower() == "exit":
            print("Thank you for filling our database, bro!")
            quit()
        else:
            continue
        

if __name__ == '__main__':
    run()