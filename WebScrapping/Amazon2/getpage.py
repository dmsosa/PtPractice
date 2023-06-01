def run():
    from requests_html import HTMLSession
    from bs4 import BeautifulSoup

    s = HTMLSession()
    url = 'https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A172635&language=es&ref=nav_em__nav_desktop_sa_intl_printers_0_2_6_11'
    req = s.get(url)


    def getdata(url):
        try:
            soup = BeautifulSoup(req, 'html.parser')
            print(soup.find('title').string)
            return soup

        except Exception as err:
            print(err)
            return

    def getpage(soup):
        ul = soup.find('span', {'class':'s-pagination-strip'})
        if not ul.find('span', {'class':'s-pagination-item s-pagination-next s-pagination-disabled'}):
            last = ul.find('span', {'class':'s-pagination-item s-pagination-disabled'}).string
            url = 'https://www.amazon.com/'+ str(ul.find('a', {'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
            print("page " + url.split('page')[1][1:1] + "out of "+last+"!")
            print(url)
            return url
        else:
            print("this is the last page! ("+last+").")
    soup = getdata(url)
    next = getpage(soup)
if __name__ == '__main__':
    run()