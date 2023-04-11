from bs4 import BeautifulSoup 
import requests

dinge = input("Welche Dinge mochtest du suchen?\n")
url = "https://www.newegg.com/p/pl?d=%s" %(dinge)

uh = requests.get(url).text 
soup = BeautifulSoup(uh, 'html.parser')

#Ermitteln der Seitenzahl dieses Seit

a = soup.find("div", class_="list-tool-pagination").children
for i in a:
    print(i)