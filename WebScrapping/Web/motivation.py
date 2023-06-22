from bs4 import BeautifulSoup
import http.client
import re
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


conn = http.client.HTTPSConnection('www.riminitoday.it')
conn.request(method="GET",url='/social/frasi-motivazionali-per-sentirsi-meglio.html')
r = conn.getresponse()
html = r.read().decode()

soup = BeautifulSoup(html, 'html.parser')
h2 = soup.find_all('h2')[1:]
headers = list()
for h in h2:
    headers.append(h.text)
phrases = soup.find_all('p')
phraseBook = dict()
for p in phrases:
    try:
        sentence = re.search('[0-9]+(.*)', p.text).group().split('(')
        phrase = sentence[0]
        author = sentence[1][:-1].split(",")[0]
        phraseBook[phrase] = author
    except: continue

with open('./phrases.xml', 'w',encoding='utf-8') as f:

    i = 0
    c = 0

    f.write('<ul class="{}">\n'.format(headers[i]))
    for k,v in phraseBook.items():
        f.write('  <li>\n    <p>'+k+'</p>\n    <a>'+v+'</a>\n  </li>\n')
        c += 1
        if c == 40:
            continue
        if c % 10 == 0:
            i += 1
            f.write('</ul>\n<ul class="{}">\n'.format(headers[i]))
    f.write('</ul>')

print('File written!')