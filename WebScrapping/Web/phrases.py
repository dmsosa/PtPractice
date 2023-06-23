from bs4 import BeautifulSoup
import http.client, json, urllib.parse

def set_quotes():
        with open('./phrases.xml', 'r', encoding='utf-8') as f:
            xml = f.read()
            soup = BeautifulSoup(xml, 'lxml')
            phrases = soup.find_all('li')
            quotes = dict()
            for phrase in phrases:
                quote = phrase.p.text
                author = phrase.a.text
                quotes[quote] = author
            return quotes

def ubersetzer(src, ziel, text):
    assert (type(src) == str and type(ziel) == str) and (len(src) == 2 and len(ziel) == 2), f'Ungultiger Landercode! "{src}", "{ziel}"'

    text = urllib.parse.quote(text)
    src_lang = src.lower()
    ziel_lang = ziel.lower()
    api_key = 'f26fbfc3c5msh0ed852bd7999cdbp14fd28jsnec2403b96d20'
    host = 'text-translator2.p.rapidapi.com'
    payload = f'source_language={src_lang}&target_language={ziel_lang}&text={text}'
    headers = {
         'X-RapidAPI-Key': api_key,
         'X-RapidAPI-Host': host,
         'content-type': 'application/x-www-form-urlencoded'
    }
    #mit dem API verbinden
    conn = http.client.HTTPSConnection(host)
    conn.request('POST', '/translate', payload, headers)
    response = conn.getresponse()
    js = json.loads(response.read())

    return js['data']['translatedText']

def translator(iterable, translator=ubersetzer, lang='de'):
    translated_phrases = dict()
    for phrase, author in iterable.items():
        translated = ubersetzer('it', lang, phrase)
        translated_phrases[translated] = author
    return translated_phrases
         
     
def run():
    quotes = set_quotes()
    ziel_lang = input('In welche Sprache mochten Sie die Absatzen ubersetzen?\n')
    if len(ziel_lang) < 1: ziel_lang = 'de'
    translated_quotes = translator(quotes, lang=ziel_lang)
    for q,v in translated_quotes.items():
        print(q,v)

if __name__ == '__main__':
    run()