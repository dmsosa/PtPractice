def run():
    from bs4 import BeautifulSoup
    import requests
    # import sys
    # sys.stdin.reconfigure(encoding='utf-8')
    # sys.stdout.reconfigure(encoding='utf-8')
    Found = False

    url = 'https://en.wikipedia.org/wiki/{name}'
    while not Found:
        char = input("Which person do you want to look for?")
        if char.lower() == "exit":
            print("Thanks for programming!")
            return
        characters = char.split()
        person_name = ""
        count = 0
        for c in characters:
            if count > 0:
                person_name += c.capitalize()+" "
            else:
                person_name += c.capitalize()+" "
            count += 1
        person_name = person_name.replace(" ","_")[:-1]
        uhandle = requests.get(url.format(name = person_name))
        try:
            soup = BeautifulSoup(uhandle.text, 'html.parser')
            if (no_content := soup.find('div', id='noarticletext_technical')) is not None:
                print("This article do not exists!")
                continue
            d = soup.find('div', class_="shortdescription nomobile noexcerpt noprint searchaux")
            print(d.text)
        except:
            pass
    # print(soup.prettify())
    # content = soup.find(class_ = "mw-parser-output")
    # print(content)
    #     # print(pi)
if __name__ == '__main__':
    run()