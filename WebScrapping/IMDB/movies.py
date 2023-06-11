from bs4 import BeautifulSoup
import urllib.error, urllib.parse, urllib.request
import re, openpyxl
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
uh = urllib.request.urlopen(url, context=ctx)
headers = uh.info()
html = uh.read()
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Top Rated Filmen"
sheet.append(['Rank', 'Name', 'Year', 'Rating'])
# print(headers)

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('tbody', class_="lister-list").find_all('tr')
for m in table:
    info = m.find(class_='titleColumn')
    actors = info.find('a')['title']
    name = info.find('a').text
    pos = info.get_text(strip=True).split('.')[0]
    year = info.find('span').text.strip('()')
    ratinfo = m.find(class_='ratingColumn imdbRating').strong['title']
    ratinfo = re.search("(?P<rating>\s\S.+)", ratinfo).group('rating').lstrip()
    rating = m.find(class_='ratingColumn imdbRating').strong.text
    sheet.append([pos, name, year, rating])

print('Filmen gespeichernt!')
excel.save('Top Rated Filmen.xlsx')
    