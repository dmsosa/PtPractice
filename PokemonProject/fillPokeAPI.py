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




    # fill = input("which data do you want to fill up in our pokedex?")
    # if fill.lower() == "pokemon":
    #     fillPokemon()
    # if fill.lower() == "evos":
    #     fillEvos()
    
    todo = input("Which Data do you want to fill up?")
    if len(todo) < 1:
        fillEvos()

if __name__ == '__main__':
    run()