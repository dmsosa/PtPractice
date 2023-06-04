def run():
     
    import re
    url = 'https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A24046923011%2Cn%3A172541&dc&page=400&language=es&qid=1685691414&ref=sr_pg_3'
    
    url = 'https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A24046923011%2Cn%3A172541&dc&language=es&qid=1685691446&ref=sr_pg_1'


    def getdata(url):
        HEADERS = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"}
        from requests_html import HTMLSession
        from bs4 import BeautifulSoup
        try:
            s = HTMLSession()
            req = s.get(url, headers=HEADERS)
            req.html.render(sleep=1)
            soup = BeautifulSoup(req.html.html, 'html.parser')
            print(soup.find('title').string)
            return soup

        except Exception as err:
            print(err)
            return

    def getpage(soup):
        from requests_html import HTMLSession
        from bs4 import BeautifulSoup
        ul = soup.find('span', {'class':'s-pagination-strip'})
        if not ul.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator', 'aria-disabled':"true"}):
            last = ul.find('span', {'class':'s-pagination-item s-pagination-disabled', 'aria-disabled':'true'}).string
            next_url = 'https://www.amazon.com/'+ str(ul.find('a', {'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
            try:
                current_page = re.search("\d+",re.search("page=[0-9]+&",url).group()).group()
            except:
                current_page = 1
            print("current page: ", current_page)
        else:
            next_url = None
            last = ul.find('span', class_='s-pagination-item s-pagination-selected').string
            print("this is the last page! ("+last+").")
        return next_url
    
    while True:
        soup = getdata(url)
        url = getpage(soup)
        if not url:
            break
        else:
            print(url) 

if __name__ == '__main__':
    run()