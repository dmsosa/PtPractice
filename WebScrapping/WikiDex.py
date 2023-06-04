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

cur.execute("""SELECT url FROM Webs ORDER BY RANDOM() LIMIT 1""")
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

#Retrieving an unretrieved url randomly
cur.execute("""SELECT id, url FROM Pages WHERE html is NULL AND error is 0 ORDER BY RANDOM() LIMIT 1""")
row = cur.fetchone()
fromid = row[0]
url = row[1]

print(url)
r = urllib.request.urlopen(url, context=ctx)
html = r.read()

print(len(html), "characters retrieved!")

if r.getcode() != '200':
    print('Error!', r.getcode())
    cur.execute('UPDATE Pages SET error = 1 WHERE url = ?', (url,))

if 'text/html' != r.info().get_content_type():
    print('this is not an html page!')
    cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
    conn.commit()

soup = BeautifulSoup(html, 'html.parser')
tags = soup.body.find_all('a')
for a in tags:
    if a.get('href') is not None:
        next_url = a['href']
