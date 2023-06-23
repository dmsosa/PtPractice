def run():
    import threading, os
    import requests, sys
    import time, random, re
    import sqlite3
    from bs4 import BeautifulSoup
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    search = None
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', "Referer":"https://www.google.com"}
 


    #Ebay search func
    def search_ebay(search, headers, products):
        print('Ebay assigned to thread {}'.format(threading.current_thread().name))
        page=1
        # while page < 20:
        
        while page < 3:
            rand_sleep = random.randint(10, 19)/10
            time.sleep(rand_sleep)
            ebay=f'https://www.ebay.de/sch/i.html?_from=R40&_nkw={search}&_sacat=0&LH_TitleDesc=0&_pgn={page}'
            try:
                req = requests.get(ebay, headers=HEADERS)
                html = req.text
            except Exception as err:
                print(err)
                return
            soup = BeautifulSoup(html, 'html.parser')

            items = soup.find('ul', class_='srp-results srp-list clearfix')
            if items is None:
                page += 1
                continue
            for item in items:
                try:
                    info = item.find(class_='s-item__info clearfix')
                    title = info.find(class_='s-item__title').text
                    price = info.find('span', class_='s-item__price').text.split()[1]
                    price = float(price.replace(",", "."))
                    products[title] = (price, 'ebay')
                except:continue
            page += 1


    #AliExpress search func
    def search_alie(search, headers, products):
        print('Alie assigned to thread {}'.format(threading.current_thread().name))
        page = 1
        while page < 3:
            rand_sleep = random.randint(10, 19)/10
            print('sleeping', rand_sleep, 'seconds')
            time.sleep(rand_sleep)
            alie=f'https://www.aliexpress.com/af/{search}.html?SearchText={search}&catId=0&initiative_id=SB_20230617061855&spm=a2g0o.productlist.1000002.0&trafficChannel=af&g=y&page={page}'
            try:
                req = requests.get(alie, headers=HEADERS)
                html = req.text
            except Exception as err:
                print(err)
                return
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find('div', class_='list--gallery--34TropR')
            if items is None:
                page += 1
                continue
            for item in items:
                try:
                    info = item.find('div', class_='manhattan--content--1KpBbUi')
                    price = float(info.find(class_='manhattan--price-sale--1CCSZfK').text[:-1].replace(",",""))/100
                    title = info.find(class_='manhattan--title--24F0J-G cards--title--2rMisuY')['title']
                    products[title] = (price, 'alie')
                except:continue
                
            page += 1 

    #Walmart search func
    def search_walmart(search, headers, products):
        print('Walmart assigned to thread {}'.format(threading.current_thread().name))
        page = 1
        
        while page < 3:
            rand_sleep = random.randint(10, 19)/10
            time.sleep(rand_sleep)
            walmart='https://www.walmart.com/search?q=%s&page=%x&affinityOverride=default'%(search, page)
            try:
                req = requests.get(walmart, headers=HEADERS)
                html = req.text
                
            except Exception as err:
                print(err)
                return
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find('div', class_='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl')
            if items is None:
                page += 1
                continue
            for item in items:
                item = items.find()
                price = item.find('div', attrs={'data-automation-id':"product-price"}).find('div').text
                numeric_price = float(re.search('\d+.\d+',price).group().replace(",", "."))
                title = item.find('span', attrs={'data-automation-id':'product-title'}).string
                products[title] = (numeric_price, 'walmart')
            page += 1

    def definer(search):
        val = None
        conn = sqlite3.connect('ecommerce.sqlite')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Products (
        search_type TEXT,
        website TEXT,
        product_name TEXT,
        price REAL
        )''')
        while val is None:
            many = input('Wie Viele Produkt mochten Sie suchen?\n')
            if len(many) < 1:
                many = 1
            elif many.lower() == 'no':
                many = 0
                break
            try:
                val = int(many)
            except:
                print('Bitte geben Sie ein gultige Antwort!')

        while many > 0:
            search=input('Welches Produkt mochten Sie suchen?\n')
            if len(search) < 1:
                search = rand_produkte[random.randint(0, len(rand_produkte)-1)]
            rand_produkte = ['Monitor', 'CPU', 'T-shirts', 'Consoles', 'Instruments', 'Piano', 'Guittar', 'Phone','Refrigerator', 'Bookshelf', 'Candles', 'Furniture', 'Decoration']

            products = dict()
            print('ID of current main process {}'.format(os.getpid()))
            x = threading.Thread(name='t1' ,target=search_ebay(search, HEADERS, products))
            y = threading.Thread(name='t2', target=search_alie(search, HEADERS, products))
            z = threading.Thread(name='t3', target=search_walmart(search, HEADERS, products))
            x.start()
            y.start()
            z.start()
            x.join()
            y.join()
            z.join()

            print('research finished\n')

            sorted_products = sorted(products, key=lambda x:products[x][0])

            print('Top 10 cheapest {}:'.format(search))
            for p in sorted_products[:10]:
                print("Article: {} / Price: {}".format(p, products[p][0]))
            
            for k, v in products.items():
                name = k
                price = v[0]
                website = v[1]
                cur.execute('''INSERT OR IGNORE INTO Products (search_type, website, product_name, price) VALUES (?, ?, ?, ?)''', (search, website, name, price))
                conn.commit()
            print('loaded!')
            many -= 1

        conn.commit()
        cur.close()

    definer(search)
if __name__=='__main__':
    run()
    
