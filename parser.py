from bs4 import BeautifulSoup
import requests
from user_parser import ria


def parse(url):
    exceptions = {
        'https://ria.ru': ria.get,
    }

    if url in exceptions.keys():
        return exceptions[url]()

    r = requests.get(url=url)
    xml = BeautifulSoup(r.text, 'xml')
    items = xml.findAll('item')
    for item in items:
        return item.find('link').text