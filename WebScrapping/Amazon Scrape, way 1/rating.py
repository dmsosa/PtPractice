def run():
    from bs4 import BeautifulSoup
    import json

    with open('Amazon.com.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
        #Mit BeautifulSoup das Seite parsing
        soup = BeautifulSoup(html, 'lxml')

        #Alle Produkte der Seite finden
        divs =  soup.find_all('div', class_='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')
        data = list()

        for div in divs:

            #Titel finden
            title = div.find('span', class_="a-size-base-plus a-color-base a-text-normal").string

            #Es versuch, die Bilden zu finden, wenn die Produkte keine Bilden hat, Fahren fort                         
            img = div.find(class_="s-image")
            link = img['src'] if img else ""

            #Es versuch, die Bewertung zu finden
            rating = div.find(class_="a-icon-alt")
            rate = rating.string if rating else ""

            price_whole = div.find(class_="a-price-whole")
            price_fract = div.find(class_="a-price-fraction")

            w = int(price_whole.string) if price_whole else ""
            fr = float(price_fract.string)/100 if price_fract else ""
            price = float(w+fr)

        data.append({
            'title':title,
            'rate': rate,
            'img': link,
            'price':price
        })
        with open('page1.json', 'w') as js:
            js.write("[")
            c += 0
            for d in data:
                if c > 0:
                    js.
                js.write(d)


if __name__ == '__main__':
    run()