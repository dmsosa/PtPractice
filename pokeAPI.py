def run():
    import urllib.request, urllib.parse, urllib.error
    import sqlite3
    import requests
    import json
    
    # h = requests.get('https://pokeapi.co/api/v2/pokemon/charizard')
    # js = json.loads(h.text)
    # print(js['name'])
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
        pokemon = input('What Pokemon would you like to find? (insert Pokemon''s name or id!)')
        if len(pokemon) >= 3:
            break
    try:
        url = serviceurl.format(name=pokemon)
        uh = requests.get(url)

        suggestions = dict()
        for n in range(1000):
            pkmn = requests.get(serviceurl.format(name=n))
            pkdata = json.loads(pkmn.text)
            suggestName = pkdata['name']
            APid = pkdata['id']
            for types in pkdata['types']
            

            cur.execute('''INSERT OR IGNORE INTO Pokemon (name, type, ability, hidden, APId)''')
        #     commonWords = 0
        #     for i in range(len(str(pokemon))):
        #         if pokemon[i] == suggestName[i]:
        #             commonWords += 1
        #     if commonWords > 2:
        #         suggestions[suggestName] = commonWords
        # suggestList = list()
        # for k,v in suggestions.items():
        #     suggestList.append((v,k))
        # print(suggestList)
        # suggestList = sorted(suggestList, key=lambda x:x[0], reverse=True)
        # print('Perhaps you wanted to search for: "'+suggestList[0][1]+'"?')
        if uh.text == "Not Found":
            print("Not Found Error!")
            quit()
        
        print(uh.headers['Date'], "Content Length:", uh.headers['Content-Length'])
        
        #trying to solve typo errors


                
                
    except:
        pass

if __name__ == '__main__':
    run()