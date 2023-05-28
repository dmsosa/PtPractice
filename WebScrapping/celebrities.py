from bs4 import BeautifulSoup
import requests
# import sys
# sys.stdin.reconfigure(encoding='utf-8')
# sys.stdout.reconfigure(encoding='utf-8')

url = 'https://en.wikipedia.org/wiki/{name}'
char = input("Which person do you want to look for?")
characters = char.split()
person_name = ""
count = 0
for c in characters:
    if count > 0:
        person_name += c.capitalize()+" "
    else:
        person_name += c.capitalize()+" "
    count += 1
print(person_name)
person_name = person_name.replace(" ","_")[:-1]
print(person_name)
uhandle = requests.get(url.format(name = person_name), 'utf-8')

soup = BeautifulSoup(uhandle.text, 'html.parser')
print(soup.prettify())
# print(soup.prettify())
# content = soup.find(class_ = "mw-parser-output")
# print(content)
#     # print(pi)