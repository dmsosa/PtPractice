def run():
    import sys
    from bs4 import BeautifulSoup
    from urllib import parse, request, error
    import re

    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    url = 'https://www.wikidex.net/wiki/WikiDex'
    pos = url.rfind("/")
    print()
    r = request.urlopen(url)
    headers = r.info()
    html = r.read()
    ctlen = re.search("Content-Length: (\d+)",str(headers)).group().split()[1]
    print(ctlen)
    
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.body.find_all('a')
    for a in tags:
        if a.get('href') is not None:
            up = parse.urlparse(a['href'])
            print(up, "next!!")

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