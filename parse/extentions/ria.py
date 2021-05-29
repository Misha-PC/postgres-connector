import requests
from bs4 import BeautifulSoup


def ria():
    url = 'https://ria.ru'
    r = requests.get(url=url)
    html = BeautifulSoup(r.text, 'html.parser')

    for item in html.findAll('div', class_='cell-list__item m-no-image'):
        return item.find('a', class_='cell-list__item-link')['href']
