#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from utility_common import *


def get_index():
  main_url = 'http://www.wuxiaworld.com/'
  main_page = get_page(main_url)
  soup = BeautifulSoup(main_page, 'lxml')
  items = soup.find('nav').findAll('a')
  items = filter(lambda item: 'index' in item['href'], items)
  links = []
  for item in items:
    title = str(strip_unicode(item.text)).replace(' ()', '')
    link = item['href']
    links.append([title, link, 'http://www.wuxiaworld.com/feed/'])
  links.sort()
  return links
