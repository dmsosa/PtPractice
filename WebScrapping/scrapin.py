#Retrieving articles from Newegg, and inserting the products and prices into a database, related by its primary keys
#Some comments are in german, ignore it, they just are asking for input, or telling you what's going on with the program



from bs4 import BeautifulSoup 
import sqlite3
import requests
import re

if __name__ == "__main__":
    conn = sqlite3.connect("Prices.sqlite")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Products (
        p_id INTEGER PRIMARY KEY UNIQUE, 
        name TEXT UNIQUE)
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS Prices (
        price_id INTEGER PRIMARY KEY UNIQUE, 
        p_id INTEGER,
        qty REAL)""")
    
    dinge = input("Welche Dinge mochtest du suchen?\n")
    dinge = dinge.capitalize()
    url = "https://www.newegg.com/p/pl?d=%s" %(dinge)

    uh = requests.get(url).text 
    soup = BeautifulSoup(uh, 'html.parser')

    #Ermitteln der Seitenzahl dieses Seit
    #Getting the number of pages of this website

    try:
        a = soup.find(class_="list-tool-pagination").strong
        page_num = str(a).split("/")[-2].split(">")[-1][:-1]
        print(page_num, "pages")
    except AttributeError:

        print("1 page")
   

    for p in range(1, 2):
        url = f"https://www.newegg.com/p/pl?N=4131&d={dinge}&page={p}"
        uh = requests.get(url).text
        souphand = BeautifulSoup(uh, "html.parser")
        #des Namens der Produkte erhalten
        #Getting the name of the product
        try:
            items = souphand.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell").find_all(text=re.compile(dinge))
            price_box = souphand.find(class_="price-current")
        except AttributeError:
            # Beheben unewartete Fehler, Haufige Fehler beheben   
            # Solving unexpected errors, solving common errors
            items = soup.find(class_="sc-gsDKAQ bvKObo").find_all(text=re.compile(dinge))

        print(len(items))
        for item in items:
            parent = item.parent
            if parent.name != "a":
                continue

            link = parent['href']
            price_container = item.find_parent(class_="item-container")
            zahl_price = price_container.find(class_="price-current").strong.string
            zahl_price = zahl_price.replace(",","")
            dot = price_container.find(class_="price-current").sup.string
            price = float(zahl_price+dot)
            
            cur.execute('''INSERT INTO Products 
            SELECT * FROM (SELECT (?) AS name) AS new_item
            WHERE NOT EXISTS (SELECT name FROM Products WHERE name = (?))''', (item, item))
            cur.execute('''SELECT p_id FROM Products WHERE name = (?) LIMIT 1''', (item, ))
            row = cur.fetchone()
            product_id = row[0]
            cur.execute('''INSERT OR IGNORE INTO Prices (qty, p_id) VALUES (?, ?)''', (price, product_id))

    cur.close()
    conn.commit()
    