from bs4 import BeautifulSoup
import ssl
import urllib.request, urllib.error, urllib.parse, urllib.response
import sqlite3

conn = sqlite3.connect('parsing.sqlite')
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

cur.execute("""CREATE TABLE IF NOT EXISTS Webs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
url TEXT UNIQUE
)
""")

#checking where we left off
cur.execute("""SELECT url FROM Pages WHERE error = 0 AND html is NULL ORDER BY RANDOM() LIMIT 1""")
row = cur.fetchone()
if row is not None:
    print('Restarting existing crawl')
else:
    start = input('Insert the starting url or press enter!')
    if len(start) < 1:
        start = 'https://www.wikidex.net/wiki/WikiDex'
        web = start
    elif start.endswith('.html') or start.endswith('.htm'):
        pos = start.rfind("/")
        web = start[:pos]
    if len(web) > 1:
        cur.execute("INSERT OR IGNORE INTO Webs (url) VALUES (?)", (web,))
        cur.execute("INSERT OR IGNORE INTO Pages (url, error, html) VALUES (?, ?, ?)", (web, 0, None))
        conn.commit()

webs = list()
cur.execute("""SELECT url FROM Webs""")
for r in cur:
    webs.append(str(r[0]))

many = 0
while True:
    if (many < 1):
        val = input("Wie viele Seiten mochtest du Crawlen?\n")
        if len(val) < 1:
            break
        many = int(val)
    many -= 1
    #Retrieving an unretrieved url randomly
    cur.execute("""SELECT id, url FROM Pages WHERE html is NULL AND error is 0 ORDER BY RANDOM() LIMIT 1""")
    try:
        row = cur.fetchone()
        fromid = row[0]
        url = row[1]
    except:
        print('no unretrieved Seiten found')
        many = 0
        break

    cur.execute('DELETE FROM Links WHERE fromid = ?', (fromid, ))

    try:
        r = urllib.request.urlopen(url, context=ctx)
        html = r.read()
    except:
        print('could not send the request!')
    print(url, "with", len(html), "characters retrieved!")
    if r.getcode() != 200:
        print('Error!', r.getcode())
        cur.execute('UPDATE Pages SET error = 1 WHERE url = ?', (url,))

    if 'text/html' != r.info().get_content_type():
        print('this is not an html page!')
        cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
        conn.commit()


    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as err:
        print(err)
        pass

    cur.execute('''INSERT OR IGNORE INTO Pages (url, error) VALUES (?, ?)''', (url, 0))
    cur.execute('''UPDATE Pages SET html = ? WHERE url = ?''', (html, url))



    tags = soup.body.find_all('a')
    count = 0
    for a in tags:
        href = a.get('href', None)
        if href is None: continue
        up = urllib.parse.urlparse(href)
        if (len(up.scheme) < 1):
            href = urllib.parse.urljoin(url, href)
        ipos = href.find('#')
        if ipos > 1: href = href[:ipos]
        if href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif'):continue
        if href.endswith('/'):href = href[:-1]
        if len(href) < 1:continue
        
        found = False
        for w in webs:
            if href.startswith(w):
                found = True
                break
        if not found:
            continue

        cur.execute('''INSERT OR IGNORE INTO Pages (url, error, html) VALUES (?, ?, ?)''', (href, 0, None))
        cur.execute('''SELECT id FROM Pages WHERE (url = ?)''', (href,))
        count += 1
        try:
            row = cur.fetchone()
            toid = row[0]
        except:
            print('could not retrieve')
            continue
        cur.execute('''INSERT OR IGNORE INTO Links (fromid, toid) VALUES (?, ?)''', (fromid, toid))
    print(count, 'new webs found!')
conn.commit()
cur.close()