def run():
    import sqlite3

    conn = sqlite3.connect('pokedex.sqlite')
    cur = conn.cursor()
    serviceurl = "https://pokeapi.co/api/v2/pokemon/{name}/"
    while True:
        pokemon = input('What Pokemon would you like to find? (insert Pokemon''s name or id!)\n')
        if len(pokemon) >= 3:
            break

    try:
        url = serviceurl.format(name=pokemon)
        uh = requests.get(url)
        if uh.text == "Not Found":
            try:
                suggestions = dict()
                sorted_suggestion = list()
                cur.execute("SELECT name FROM Pokemon")
                pokemon = pokemon.lower()
                for poke in cur:
                    name = poke[0]
                    commonLetter = 0
                    if len(name) != len(pokemon) and len(name) < len(pokemon):
                        continue
                    if pokemon[:3] not in name:
                        continue
                    if not name.startswith(pokemon):
                        continue
                    for letter in range(len(name)):
                        try:
                            if name[letter+name.index(pokemon)] == pokemon[letter]:
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
                        quit()
                    if typo.lower() == "yes":
                        pokemon = sorted_suggestion[0][1]
                        print("searching "+pokemon+" data...")
                        quit()
                        # url = serviceurl.format(name=pokemon)
                        # uh = requests.get(url)
            except IndexError:
                print("this pokemon is not in our pokedex!\n")
                quit()
            except Exception as err:
                print(err)
                quit()
        

            
             


        #     cur.execute('''INSERT OR IGNORE INTO Pokemon (name, type, ability, hidden, APId)''')
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

        
        # print(uh.headers['Date'], "Content Length:", uh.headers['Content-Length'])
        
        # #trying to solve typo errors


                
                
    except:
        pass

if __name__ == '__main__':
    run()