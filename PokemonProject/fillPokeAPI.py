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
        print("a")
        # for n in range (1, 100+1):
        #     f = requests.get(f'https://pokeapi.co/api/v2/evolution-chain/{n}/')
        #     js = json.loads(f.text)
        #     name = js['chain']['species']['name']
        #     if name == "eevee":
        #         print("We caught eevee!", js['id'])

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

        cur.execute('''CREATE TABLE IF NOT EXISTS Abilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        effect TEXT,
        de_name TEXT NOT NULL UNIQUE,
        pokemon_with INTEGER,
        pokemon_hidden INTEGER
        )''')

        while True:
            many = input("How many abilities do you want to look for?\n")
            try: 
                many = int(many)
            except:
                continue
            if many == 0:
                print("You think you are funny, right?\n")
                quit()
            else:
                break

        while many > 0:
            answer = ""
            ab = input("Insert ability name, bitte!\n")
            many -= 1
            try:
                uh = requests.get(serviceurl.format(ab))
                js = json.loads(uh.text)
                if uh.text.lower() == 'not found' or (len(ab) < 1):
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
                    if len(cur.fetchone()[0]):
                        print("That ability was already retrieved")
                        continue
                except TypeError:
                    pass

                try:
                    uh = requests.get(serviceurl.format(ab))
                except Exception as err:
                    print(err)
                    many -= 1
                    continue
                many -= 1

                js = json.loads(uh.text)
            try:
                for name in js['names']:
                    if name['language']['name'] == "de":
                        de_name = name['name']
                for effect in js['effect_entries']:
                    if effect['language']['name'] == "de":
                        de_effect = effect['effect']
                print(de_name, de_effect)
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

                for v in poke_with.values():
                    if v == 1:
                        poke_hid += 1
                    else: 
                        poke_no_hid += 1
            
                cur.execute('''INSERT OR IGNORE INTO Abilities (name, effect, de_name, pokemon_with, pokemon_hidden)
                VALUES (?, ?, ?, ?, ?)''', (ab, de_effect, de_name, poke_no_hid, poke_hid))
                print("new ability added to our pokedex")
            except KeyError:
                pass
            


        conn.commit()
        cur.close()
        return

    todo = input("Which Data do you want to fill up?")
    if len(todo) < 1:
        fillAbs()
        

if __name__ == '__main__':
    run()