#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from utility_common import *


def get_index():
  page = get_page('http://gravitytales.com/')
  soup = BeautifulSoup(page, 'lxml')
  soup = soup.find('ul', {'class': 'navbar-nav'})
  soup = soup.find('ul', {'class': 'dropdown-menu'})
  links = soup.findAll('a')
  links = [[str(strip_unicode(link.text)), link['href']] for link in links]
  links = filter(lambda link: link[1].startswith('/novel/'), links)
  links = [[link[0], 'http://gravitytales.com' + link[1], 'http://gravitytales.com/feed/' + link[1][7:]] for link in links]
  links.sort()
  return links
