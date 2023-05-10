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

        conn = sqlite3.connect("pokedex.sqlite")
        cur = conn.cursor()
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Evochain (
        chid INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
        first INTEGER,
        second INTEGER,
        third INTEGER
        )''')

        url = "https://pokeapi.co/api/v2/pokemon/{name}/"
        cur.execute("SELECT APId FROM Pokemon")
        for poke in cur:
            pokeid = poke[0]
            uh = requests.get(url.format(name=pokeid))

    fill = input("which data do you want to fill up in our pokedex?")
    if fill.lower() == "pokemon":
        fillPokemon()
    if fill.lower() == "evos":
        fillEvos()
    
if __name__ == '__main__':
    run()