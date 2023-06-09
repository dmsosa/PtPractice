from bs4 import BeautifulSoup
import ssl
import urllib.request, urllib.error, urllib.parse, urllib.response
import sqlite3

conn = sqlite3.connect('2.sqlite')
cur = conn.cursor()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cur.execute("""CREATE TABLE IF NOT EXISTS Pages (
id INTEGER PRIMARY KEY AUTOINCREMENT,
url TEXT,
html TEXT,
error INTEGER
)
""")

cur.execute("""CREATE TABLE IF NOT EXISTS Links (
fromid INTEGER,
toid INTEGER,
UNIQUE (fromid, toid)
)
""")

cur.execute('SELECT id, url FROM Pages WHERE html is NULL and error = 0')
row = cur.fetchone()
if row is not None:
    print('returning')
else:
    start = input('Insert the starting url or press enter!')
    if len(start) < 1:
        start = 'https://www.wikidex.net/wiki/WikiDex'
        web = start
    elif start.endswith('.html') or start.endswith('.htm'):
        pos = start.rfind("/")
        web = start[:pos]
    if len(web) > 1:
        cur.execute("INSERT OR IGNORE INTO Pages (url, error, html) VALUES (?, ?, ?)", (web, 0, None))
        conn.commit()

webs = list()
cur.execute('SELECT url FROM Pages')
for i in cur:
    webs.append(str(i[0]))

many = 0

while True:
    if many < 1:
        val = input("how many?")
        if len(val) < 1:break
        many = int(val)
    
    many -= 1
    cur.execute('SELECT id, url FROM Pages WHERE html is NULL and error = 0 ORDER BY RANDOM() LIMIT 1')
    try:
        row = cur.fetchone()
        fromid = row[0]
        url = row[1]
    except:
        print('No unretrieved pages')

    cur.execute('DELETE FROM Links WHERE fromid = ?', (fromid, ))

    try:
        r = urllib.request.urlopen(url, context=ctx)
        html = r.read()
    except:
        pass

    print(url, "with", len(html), "characters retrieved!")

    if r.getcode() != 200:
        print('Error!', r.getcode())
        cur.execute('UPDATE Pages SET error = 1 WHERE url = ?', (url,))
        conn.commit()

    if 'text/html' != r.info().get_content_type():
        print('this is not an html page!')
        cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
        conn.commit()

    soup = BeautifulSoup(html, 'html.parser')

    cur.
    tags = soup.body.find_all('a')

    count = 0
    for a in tags:
        href = a.get('href', None)
        if href is None: continue
        up = urllib.parse.urlparse(href)
        if len(up.scheme) < 1: href = urllib.parse.urljoin(url,href)
        ipos = href.find('#')
        if ipos > 0: href = href[:ipos]
        if href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif'):continue
        if href.endswith('/'):href = href[:-1]
        if len(href) < 1:continue
        found = False
        for w in webs:
            if href.startswith(w):
                found = True
                break
            if not found:continue
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, error) VALUES (?, ?, ?)', (href, None, 0))
        cur.execute('SELECT id FROM Pages WHERE url = ?',(href,))
        row = cur.fetchone()
        toid = row[0]
        cur.execute('''INSERT OR IGNORE INTO Links (fromid, toid) VALUES (?, ?)''', (fromid, toid))

    print(count)

conn.commit()
cur.close()