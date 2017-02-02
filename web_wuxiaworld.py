#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re


url = 'http://www.wuxiaworld.com/emperor-index/'


def get_page(url):
  req = urllib2.Request(url , headers={'User-Agent': 'Magic Browser'})
  return urllib2.urlopen(req).read()

def find_links(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  article = soup.find('article')
  links = [a['href'] for a in article.findAll('a')]
  links = filter(lambda link: 'www.wuxiaworld.com' in link and 'index' in link and 'chapter' in link, links)
  links = list(set(links))
  return links

def sort_links(links):
  new_links = []
  for link in links:
    slink = re.split('-|/', link)
    chapter = [int(str(s)) for s in slink if s.isdigit()]
    order = chapter[0]
    new_links.append([order, link])
  new_links.sort(key=lambda x: x[0])
  return new_links

def web_wuxiaworld():
  links = find_links(url)
  links = sort_links(links)
  links = filter(lambda link: int(link[0]) > 52, links)
  links = [link[1] for link in links]
  return links
