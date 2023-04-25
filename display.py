#Displaying top 5 cheapest producst of our database
#Anzeigen der Top 5 der gunstigsten Produkte unserer Datenbank

import sqlite3

conn = sqlite3.connect("Prices.sqlite")
cur = conn.cursor()

prices = list()
cur.execute('''SELECT DISTINCT p_id, qty FROM Prices''')
for row in cur:
    product_id = row[0]
    product_price = row[1]
    if product_price <= 0: continue
    prices.append(row)

products = dict()

for tuple in prices:
    product_id = tuple[0]
    price = tuple[1]
    try:
        cur.execute("SELECT name FROM Products WHERE p_id = (?)",(product_id,))
        name = cur.fetchone()[0]
    except:
        continue

    if not name: continue
    products[name] = price

sorted_products = sorted(products, key = lambda item : products.get(item))

for i in range(5):
    print(sorted_products[i], end="")
    for j in range(3):
        print("    ", end="")
    print(products[sorted_products[i]])
    

cur.close()