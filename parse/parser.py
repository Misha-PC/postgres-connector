from bs4 import BeautifulSoup
import requests


def ria():
    url = 'https://ria.ru'
    r = requests.get(url=url)
    html = BeautifulSoup(r.text, 'html.parsers')

    for item in html.findAll('div', class_='cell-list__item m-no-image'):
        return item.find('a', class_='cell-list__item-link')['href']


def parse(url):
    print("***** parse ", url)
    exceptions = {
        'https://ria.ru': ria,
    }

    if url in exceptions.keys():
        return exceptions[url]()

    r = requests.get(url=url)
    xml = BeautifulSoup(r.text, 'xml')
    items = xml.findAll('item')
    for item in items:
        print("***** end ")
        return item.find('link').text


if __name__ == '__main__':
    parse(r'https://ria.ru')