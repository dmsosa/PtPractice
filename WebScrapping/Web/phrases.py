from bs4 import BeautifulSoup
import http.client

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

def ubersetzer(lang, text):
    assert for lang in code type(lang) == str and len(lang) == 2, f'Ungultiger Landercode! "{lang}"'
    text = text.encode()
    api_key = 'f26fbfc3c5msh0ed852bd7999cdbp14fd28jsnec2403b96d20'
    host = 'text-translator2.p.rapidapi.com'
    payload = f'source_language=en&target_language={lang}&text={text}'
    headers = {
         'X-RapidAPI-Key': api_key,
         'X-RapidAPI-Host': host,
         'content-type': 'application/x-www-form-urlencoded'
    }
    #mit dem API verbinden
    conn = http.client.HTTPSConnection(host)
    conn.request('POST', '/translate', payload, headers)
    response = conn.getresponse()
    translation = response.read().decode('utf-8')
    return translation

def run():
    quotes = set_quotes()
    source_lang = input('In welcher Sprache schreiben Sie?')
    phrase = input('Geben Sie bitte ein Absatz und ein Landercode')
    ziel_lang = input('In welche Sprache mochten Sie es ubersetzen?')
    codes = [source_lang, ziel_lang]
    print(ubersetzer(code, phrase))

if __name__ == '__main__':
    run()