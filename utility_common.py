#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


def strip_unicode(text):
    return ''.join(i for i in text if ord(i)<128).strip()

def get_page(url):
  req = urllib2.Request(url , headers={'User-Agent': 'Magic Browser'})
  req = urllib2.urlopen(req)
  page = req.read()
  req.close()
  return page

def find_links(link_url, starting, includes, excludes=[]):
  page = get_page(link_url)
  soup = BeautifulSoup(page, "lxml")
  article = soup.find('article')
  links = [a['href'] for a in article.findAll('a')]
  links = filter(lambda link: link.startswith(starting), links)
  for include in includes:
    links = filter(lambda link: include in link, links)
  for exclude in excludes:
    links = filter(lambda link: exclude not in link, links)
  links = list(set(links))
  return links
