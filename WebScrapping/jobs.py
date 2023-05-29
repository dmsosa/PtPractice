def run():
    from bs4 import BeautifulSoup
    import requests
    html = requests.get('https://www.upwork.com/nx/jobs/search/?q=django&sort=recency')
    soup = BeautifulSoup(html.text, 'lxml')
    job = soup.find('h3', class_='my-0 p-sm-right job-tile-title')
    print(job)


if __name__ == '__main__':
    run()