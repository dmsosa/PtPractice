from bs4 import BeautifulSoup 
import requests
import re

dinge = input("Welche Dinge mochtest du suchen?\n")
dinge = dinge.capitalize()
url = "https://www.newegg.com/p/pl?d=%s" %(dinge)

uh = requests.get(url).text 
soup = BeautifulSoup(uh, 'html.parser')

#Ermitteln der Seitenzahl dieses Seit

a = soup.find(class_="list-tool-pagination").strong
page_num = str(a).split("/")[-2].split(">")[-1][:-1]
print(page_num)

for p in range(1, 2):
    url = f"https://www.newegg.com/p/pl?N=4131&d={dinge}&page={p}"
    uh = requests.get(url).text
    souphand = BeautifulSoup(uh, "html.parser")
    #des Namens der Produkte erhalten

    div = souphand.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(dinge))
    print(len(items))
    for item in items:
        print(item)
