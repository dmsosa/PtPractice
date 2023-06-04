def getdata():
    from bs4 import  BeautifulSoup
    from urllib import parse, request, error
    import re
    import os
    #Der Seite, von den wir die Datei beziehen
    url = 'https://galgenraten.net/galgenraten-w%C3%B6rter'

    r = request.urlopen(url)
    headers = r.info()
    html = r.read()
    os.system('cls')
    soup = BeautifulSoup(html, 'html.parser')

    h1 = soup.body.h1.contents[0]
    br = soup.body.h1.span.string
    print(h1)
    print(br)

    worter = soup.find_all('code')
    with open('./data.txt', 'w', encoding='utf-8') as f:
        c = 0
        for w in worter:
            if c > 0:
                f.write("\n"+w.string)
            else:
                f.write(w.string)
            c += 1
        f.close()
    print("Wir sind fertig!")

def run():
    getdata()

if __name__ == '__main__':
    run()

