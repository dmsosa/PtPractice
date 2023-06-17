import threading
import requests
from bs4 import BeautifulSoup
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
ecommerces = ['ebay', 'amazon', 'walmart', 'avito', 'aliexpress']

search=input('Welches Produkt mochten Sie suchen?')

def search_ebay(search, headers):
    
    page=1
    products=dict()
    # while page < 20:
    
    while page < 3:
        ebay=f'https://www.ebay.de/sch/i.html?_from=R40&_nkw={search}&_sacat=0&LH_TitleDesc=0&_pgn={page}'
        try:
            re = requests.get(ebay, headers=HEADERS)
            html = re.text
        except Exception as err:
            print(err)
            return
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('ul', class_='srp-results srp-list clearfix')
        for item in items.children:
            try:
                info = item.find(class_='s-item__info clearfix')
                title = info.find(class_='s-item__title').text
                price = info.find('span', class_='s-item__price').text.split()[1]
                price = float(price.replace(",", "."))
                products[title] = price
            except:continue
        page += 1
    
    return products
#unsere seiten

def search_alie(search, headers):
    page = 1
    products = dict()
    while page < 5:
        alie=f'https://www.aliexpress.com/af/{search}.html?SearchText={search}&catId=0&initiative_id=SB_20230617061855&spm=a2g0o.productlist.1000002.0&trafficChannel=af&g=y&page={page}'
        try:
            re = requests.get(alie, headers=HEADERS)
            html = re.text
        except Exception as err:
            print(err)
            return
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('div', class_='list--gallery--34TropR')
        for item in items:
            try:
                info = item.find('div', class_='manhattan--content--1KpBbUi')
                price = float(info.find(class_='manhattan--price-sale--1CCSZfK').text[:-1].replace(",",""))/100
                title = info.find(class_='manhattan--title--24F0J-G cards--title--2rMisuY')['title']
                products[title] = price
            except:continue
            
        page += 1 
    return products

def search_walmart(search, HEADERS):

# walmart='https://www.walmart.com/search?q=%s}'%search

ebay_products = search_ebay(search, HEADERS)
alie_products = search_alie(search, HEADERS)

print(alie_products)
# ebay_products = search_ebay(search, HEADERS)

