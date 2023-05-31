def run():
    import json
    with open("./page1.json","r") as file:
        js = json.load(file)
        titpri = dict()
        for item in js:
            titpri[item['title']] = item['price']
        
        print('top 10 cheapest products')
        c = 0
        for product in sorted(titpri, key= lambda x:titpri[x]):
            if c > 10:
                break
            print(product, titpri[product])
            c += 1 
            

if __name__ == "__main__":
    run()   