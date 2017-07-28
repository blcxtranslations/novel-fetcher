#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from utilities.utility_common import strip_unicode, get_page


def get_index(url):
    import re
    try:
        found = re.search('(https://www.fanfiction.net/s/[0-9]*/)*', url).group(1)
    except AttributeError:
        found = url
    book_url = found
    book_page = get_page(book_url)
    soup = BeautifulSoup(book_page, 'lxml')
    items = soup.findAll('option')
    items = list(set(items))
    links = []
    print len(items)
    for item in items:
        # title = str(strip_unicode(item.text)).replace('[0-9]*. ', '')
        title = str(strip_unicode(item.text))
        link = book_url + str(item['value'])
        if link not in links:
            links.append([title, link, book_url])
        links.sort()
    return links
