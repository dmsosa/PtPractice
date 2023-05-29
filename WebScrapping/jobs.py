def run():
    from bs4 import BeautifulSoup
    from urllib import request
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
    import urllib.parse
    import requests
    url = 'https://www.upwork.com/nx/jobs/search/?q=django&sort=recency'
    API_KEY = 'a3da6ccc-cf81-4f5b-8a8d-b57f240e2b5c'


    HEADERS = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    
    try:
        page = requests.get(url, params = {'api_key' : API_KEY, 'url' : url}, headers={'User-Agent':HEADERS})
        soup = BeautifulSoup(page.text, 'html.parser')
        print(soup.find('title').text)
    except HTTPError as e:
        print(e)

if __name__ == '__main__':
    run()