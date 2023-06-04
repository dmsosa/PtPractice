def run():
    from bs4 import BeautifulSoup
    from urllib import parse, request, error

    r = request('https://www.wikidex.net/wiki/WikiDex')
    print(r.info())
    # import json
    # with open("./page1.json","r") as file:
    #     js = json.load(file)
    #     titpri = dict()
    #     for item in js:
    #         titpri[item['title']] = item['price']
        
    #     print('top 10 cheapest products')
    #     c = 0
    #     for product in sorted(titpri, key=lambda x:titpri[x]):
    #         if c > 10:
    #             break
    #         print(product, titpri[product])
    #         c += 1 
            

if __name__ == "__main__":
    run()   