from bs4 import BeautifulSoup
from parse.extentions.ria import ria
import requests


def parse(url):
    exceptions = {
        'https://ria.ru': ria,
    }

    if url in exceptions.keys():
        return exceptions[url]()

    r = requests.get(url=url)
    xml = BeautifulSoup(r.text, 'xml')
    items = xml.findAll('item')
    for item in items:
        return item.find('link').text
